# import asyncio
import socket
import functools
from _thread import *
import pickle
from .game import Game, Player
import sys

ip = '127.0.0.1'
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((ip, port))
except socket.error as e:
    str(e)

server.listen()
print("Waiting for a connection, Server Started")


NUMBER_OF_PLAYERS = 3

connected = set()
games = {}
idCount = 0

def handler(conn, player=None, gameId=None):
    """
    Handle the client.
    :param conn: Connection with client
    :param player: The player.
    :param gameId: The game id.
    """
    global idCount
    global games

    # Send the player the player id.
    conn.send(str.encode("Player #"+str(player.id)))
    # Add the player to the game.
    if gameId in games:
        game = games[gameId]
    else:
        print("Room connection error. The room got deleted?")
        conn.send(str.encode("Connection lost. Server error"))
        return
    
    game.add_player(player)
    dc = 0
    while dc < 10:
        name = conn.recv(4096*10)# "name,<actual_name>"
        print(name.decode())
        print(name)
        dc += 1
    # print(help(type(name)))

    if name.split(",")[0] != "name":
        conn.send(str.encode("Wrong format. Loosing connection"))
        print("Ending connection for incorrect format")
        return
    player_name = ''.join(name.split(",")[1:]) # doing a join for case of player using ',' in there name
    game.set_name(player, player_name)
    
    # only send once before getting in the main loop
    conn.send(str.encode("0,Player connected and waiting."))

    #Implement code to keep the game alive even if one player loses connection.
    while True:
        try:
            # Try to start the game if not started
            if not game.started:
                game.start()
            elif not game.running:
                game.running = True
                conn.send(str.encode("1,Game started"))
                conn.send(str.encode("2,"+game.get_category(player)))
                print("game started")
                
            if game.running: 
                data = conn.recv(4096*10)#.decode() # alright lets see
                print(data)
                data = data.decode()
                print(data)
                if game.started:
                    if data == "finished":
                        conn.send(str.encode("3,"+game.get_info()))
                        game.finished(player)
                    elif data == "drawing":
                        print("receiving drawing")
                        dimensions = conn.recv()
                        drawing_string = conn.recv()
                        print("Image received with dimensions", dimensions)
                        next_category, predicted = game.score_drawing(player, dimensions, drawing_string)
                        conn.send(str.encode("2,"+next_category+","+predicted))
                        conn.send(str.encode(game.get_info()))
                    elif data == "skip":
                        player.next_category();
                        conn.send(str.encode("2,"+game.get_category(player)))
                        
                if game.all_finished():
                    conn.send(str.encode("4,"+game.get_info()))
                    game.reset()
        except:
            print("except break")
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    
def start_server():
    global idCount
    global server

    while True:
        conn,addr = server.accept()
        print("Connected to: ", addr)
        
        idCount += 1
        playerId = (idCount - 1) % NUMBER_OF_PLAYERS + 1
        player = Player(playerId)
        gameId = (idCount - 1)//NUMBER_OF_PLAYERS
        if idCount % NUMBER_OF_PLAYERS == 1:
            games[gameId] = Game(gameId, NUMBER_OF_PLAYERS)
            print("Creating a new game...")
        start_new_thread(handler, (conn,player,gameId))

start_server()