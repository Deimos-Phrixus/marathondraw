import asyncio
import websockets
import functools
from _thread import *
import pickle
from game import Game, Player
import sys

NUMBER_OF_PLAYERS = 1

connected = set()
games = {}
idCount = 0

async def handler(websocket, path, player, gameId):
    """
    Handle the client.
    :param websocket:
    :param path:
    :param player: The player.
    :param gameId: The game id.
    """
    global idCount
    global games
    # Send the player the player id.
    #await websocket.send(str.encode(str(player.id)))
    await websocket.send("Player #"+str(player.id))
    # Add the player to the game.
    if gameId in games:
        game = games[gameId]
    else:
        print("Room connection error. The room got deleted?")
        await websocket.send("Connection lost. Server error")
        return
    
    game.add_player(player)

    name = await websocket.recv() # "name,<actual_name>"
    if name.split(",")[0] != "name":
        await websocket.send("Wrong format. Loosing connection")
        print("Ending connection for incorrect format")
        return
    player_name = ''.join(name.split(",")[1:]) # doing a join for case of player using ',' in there name
    game.set_name(player, player_name)
    
    while True:
        try:
            # Try to start the game if not started
            if not game.started:
                await websocket.send("0,Player connected and waiting.")
                game.start()
                print("connected and waiting")
            elif not game.running:
                game.running = True
                await websocket.send("1,Game started")
                await websocket.send("2,"+game.get_category(player))
                print("game started")
            if game.running: 
                data = await websocket.recv()   
                if game.started:
                    if data == "finished":
                        game.finished()
                    elif data == "drawing":
                        print("receiving drawing")
                        dimensions = await websocket.recv()
                        drawing_string = await websocket.recv()
                        print("Image received with dimensions", dimensions)
                        next_category, predicted = game.score_drawing(player, dimensions, drawing_string)
                        await websocket.send("2,"+next_category+","+predicted)
                        await websocket.send(game.get_info(player))
                    elif data == "skip":
                        player.next_category();
                        await websocket.send("2,"+game.get_category(player))
                if game.all_finished():
                    game.reset()
        except: ## Websocket Breaks. meaning connection lost
            print("except break")
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    

while True:
    idCount += 1
    playerId = (idCount - 1) % NUMBER_OF_PLAYERS + 1
    player = Player(playerId)
    gameId = (idCount - 1)//NUMBER_OF_PLAYERS
    #if not (idCount % NUMBER_OF_PLAYERS == 0):
        #games[gameId] = Game(gameId, NUMBER_OF_PLAYERS)
        #print("Creating a new game...")
        
    games[gameId] = Game(gameId, NUMBER_OF_PLAYERS)
    print("Creating a new game...")
    
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(
            functools.partial(handler, player = player, gameId = gameId), 'localhost', 5555, max_size = 2**25))
    asyncio.get_event_loop().run_forever()
