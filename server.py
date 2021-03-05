import sys
import socket
import pickle
import threading
import Participant
import re

try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except (IndexError, ValueError):
    print("IP and port must be specified. Correct usage e.g $py server.py localhost 2410")
    sys.exit()

server = socket.socket()
server.bind((ip, port))
server.listen()

clients = {}

print("Server is running...")


# broadcast to all clients:
def broadcast(sender, message):
    for c in clients:
        data = pickle.dumps((sender, message))
        c.send(data)


# constantly listen if any clients has sent any data:
def listen_for_data(c):
    while True:
        try:
            sender, message = pickle.loads(c.recv(1024))
            if not perform_command(c, message):
                broadcast(sender, message)

        except ConnectionResetError:
            leaver = clients.pop(c, Participant.Person("someone"))
            broadcast(leaver, "left the chat!")
            print(f"{leaver.name} disconnected from the server")
            c.close()
            break


# Changes done by the client must also be performed by the server to ensure that the objects are correct:
def perform_command(client, message):
    command = message.split(" ")  # create an array of the message
    if command[0] in commands:
        arg = " ".join(map(str, command[1:]))
        commands[command[0]](client, arg)
        return True
    return False


def update_name(client, new_name):
    # If a command has been performed, broadcast it to all the other clients:
    # Broadcast as bot because we don't want the bots to respond
    broadcast(Participant.Bot("server"), f"{clients[client].name} has changed their name to {new_name}")

    # Then update the clients new name:
    clients[client].name = new_name


commands = {
    '/update_name': update_name,
}

while True:
    client, (ip, port) = server.accept()  # Wait for connections
    participant = pickle.loads(client.recv(1024))  # Receive data from connected client
    print(f"{participant.name} joined from {ip}:{port}")  # Print the information for sys admins

    # So when a client is connected we add the client to a "list" of connected clients. We use dictionary since it is
    # faster to access the items
    clients[client] = participant
    threading.Thread(target=listen_for_data, args=(client,)).start()
    broadcast(Participant.Person("server"), f"{participant.name} has joined the chat!")  # Tell everybody who has joined
