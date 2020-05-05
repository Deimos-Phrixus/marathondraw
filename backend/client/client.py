import socket

# Length of the header that tells the server how big the message will be.
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Method to send message to the server from the client.
# Sending the message length first and then the message itself.
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def test():
    testing = True
    while testing:
        command = input()
        if command.lower() == "quit":
            testing = False
        else:
            send(command)

if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    test()
