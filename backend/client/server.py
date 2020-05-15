import asyncio
import websockets
import functools
from _thread import *
import pickle
from game import Game, Player
import sys

NUMBER_OF_PLAYERS = 4

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
    await websocket.send(str(player.id))
    # Add the player to the game.
    games[gameId].add_player(player)

    while True:
        #try:
        
        
        #data = await websocket.recv(4096).decode()
        data = await websocket.recv()

        if gameId in games:
            game = games[gameId]

            # Try to start the game if not started
            if not game.started:
                await websocket.send("Player connected and waiting.")
                game.start()

            if not data:
                print("if not data break")
                break
            else:
                if game.started:
                    if data == "finished":
                        game.finished()
                    elif data == "drawing":
                        dimensions = await websocket.recv()
                        drawing_string = await websocket.recv()

                        print(dimensions)
                        next_category = game.score_drawing(player, dimensions, drawing_string)

                        await websocket.send(next_category)

                    await websocket.send(game.get_info(player))
                else:
                    if data == "name":
                        name = await websocket.recv()
                        game.set_name(player, name)
                    elif data == "ready":
                        game.ready(player)

                if game.all_finished():
                    game.reset()
        else:
            print("else gameId in games break")
            break
            
            
#        except:
#            print("except break")
#            break

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
    if not (idCount % NUMBER_OF_PLAYERS == 0):
        games[gameId] = Game(gameId, NUMBER_OF_PLAYERS)
        print("Creating a new game...")

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(
            functools.partial(handler, player = player, gameId = gameId), 'localhost', 5555, max_size = 2**25))
    asyncio.get_event_loop().run_forever()
