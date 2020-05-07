import socket
from _thread import *
import pickle
from game import Game

# Replace with server IP.
server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    """
    Handle the client.
    :param conn: The connection with the client.
    :param p: The player.
    :param gameId: The game id.
    """
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_ready()
                    elif data == "ready":
                        game.ready(p)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = (idCount - 1) % 4
    gameId = (idCount - 1)//4
    if not (idCount % 4 == 0):
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True


    start_new_thread(threaded_client, (conn, p, gameId))