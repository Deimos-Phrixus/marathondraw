import asyncio
import websockets
import functools
from _thread import *
import pickle
from backend.client.game import Game, Player
import sys
from multiprocessing import Pool

NUMBER_OF_PLAYERS = 3

connected = set()
games = {}
idCount = 0

def callback():
    pass

async def message_handler(websocket, data, player, game):
    if data == "finished":
        await websocket.send("3,"+game.get_info())
        game.finished(player)
    elif data == "drawing":
        print("receiving drawing")
        dimensions = await websocket.recv()
        drawing_string = await websocket.recv()
        print("Image received with dimensions", dimensions)
        next_category, predicted = game.score_drawing(player, dimensions, drawing_string)
        await websocket.send("2,"+next_category+","+predicted)
        await websocket.send(game.get_info())
    elif data == "skip":
        player.next_category()
        await websocket.send("2,"+game.get_category(player))
    
    if game.all_finished():
        websocket.send("4,"+game.get_info())
        game.reset()

def start_game(game, playerId):
    # c = 0
    while not game.started:
        game.start()
        # if c%100==0:
        #     print("this is running for", playerId)
        # c+= 0.5

async def handler(websocket, path):
    await asyncio.sleep(1)

    global idCount
    global games

    idCount += 1
    playerId = (idCount - 1) % NUMBER_OF_PLAYERS + 1
    player = Player(playerId)
    gameId = (idCount-1)// NUMBER_OF_PLAYERS
    if idCount % NUMBER_OF_PLAYERS == 1:
        games[gameId] = Game(gameId, NUMBER_OF_PLAYERS)
        print("Creating a new game...")
    else:
        print("joining to existing game", gameId)
    await websocket.send("Attempting connection with player #"+str(player.id))
    name = await websocket.recv()
    if name.split(",")[0] != "name":
        await websocket.send("Expected user to first send name.")
        print("Loosing connection for player")
        if idCount % NUMBER_OF_PLAYERS == 1:
            del games[gameId]
        idCount -= 1
        return
    game = games[gameId]
    player_name = ''.join(name.split(",")[1:])
    game.add_player(player)
    game.set_name(player, player_name)
    await asyncio.get_event_loop().run_in_executor(None, functools.partial(start_game, game = game, playerId=playerId))
    print("this keeps happening", playerId)
    if game.started:
        await websocket.send("1, Game starting")
        await websocket.send("2,"+game.get_category(player))
      
    async for message in websocket:
        await message_handler(websocket, message, player, game)
    
    print("lost connection? ")
    idCount -= 1
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    
# def start_server():
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(
            functools.partial(handler), 'localhost', 5555, max_size = 2**25))
    print("Serving server")
    asyncio.get_event_loop().run_forever()

# start_server()