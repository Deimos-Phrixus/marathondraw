import asyncio
import websockets
import functools
from _thread import *
import pickle
from backend.game import Game, Player
import sys
from multiprocessing import Pool

NUMBER_OF_PLAYERS = 3

games = {}
idCount = 0
gameId = 0

async def message_handler(websocket, data, player, game):
    """
    Message handler. Takes message recieved from client and
    inokes appropriate change in the game.

    :param websocket: websocket object to communicate with client
    :param data: message recieved
    :param player: player object of the client
    :param game: game player is in
    """
    if data == "finished":
        await websocket.send("3, wait for all players to finish")
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
    
def start_game(game):
    """
    Loops until game is started.

    :param game: game instance that needs to start
    """
    while not game.started:
        game.start()

async def start_game_task(websocket, game):
    while not game.started:
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=0.1)
        except websockets.exceptions.ConnectionClosed:
            break
        except:
            pass
        game.start()

def finish_game(game):
    """
    Loops until game finishes.

    :param game: game instance that needs to finish
    """
    print("Lost a connection abruptly")
    while not game.all_finished():
        pass

async def handler(websocket, path):
    """
    Handler for each client connection.

    :websocket: object to communicate with client
    :path: path of the url at which player connected from
    """
    await asyncio.sleep(1)

    global idCount
    global games
    global gameId

    idCount += 1
    playerId = (idCount - 1) % NUMBER_OF_PLAYERS + 1
    player = Player(playerId)
    if idCount % NUMBER_OF_PLAYERS == 1:
        gameId += 1
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
    
    await websocket.send("0,waiting for players")
    # await asyncio.get_event_loop().run_in_executor(None, functools.partial(start_game, game = game))
    task = asyncio.create_task(start_game_task(websocket=websocket, game=game))
    await task
    if game.started:
        await websocket.send("1,Game starting")
        await websocket.send("2,"+game.get_category(player))
    
    async for message in websocket:
        await message_handler(websocket, message, player, game)
        if player.finished:
            break
        if game.all_finished():
            break
    
    ## if any player looses connection when trying to start game
    if not game.started:
        pass ## we should add handling for this

    game.finished(player)
    if not game.all_finished():
        await asyncio.get_event_loop().run_in_executor(None, functools.partial(finish_game, game=game))
    print("For player", idCount, "printed")
    await websocket.send("4,"+str(NUMBER_OF_PLAYERS)+","+game.get_info())
    try:
        del games[gameId]
        idCount -= NUMBER_OF_PLAYERS
    except KeyError:
        print("failed to remove")
        pass

# def start_server():
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(
            functools.partial(handler), 'localhost', 5555, max_size = 2**25))
    print("Serving server")
    asyncio.get_event_loop().run_forever()

# start_server()