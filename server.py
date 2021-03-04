import sys
import socket
import pickle
import threading
import Participant

try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    print("IP and port must be specified. Correct usage e.g $py server.py localhost 2410")
    sys.exit()

server = socket.socket()
server.bind((ip, port))
server.listen()

clients = {}

print("Server is running...")


def broadcast(sender, message):
    for c in clients:
        data = pickle.dumps((sender, f"{sender.name}: {message}"))
        c.send(data)


def listen_for_data(c):
    while True:
        try:
            sender, message = pickle.loads(c.recv(1024))
            broadcast(sender, message)
        except (ConnectionResetError, OSError):
            leaver = clients.pop(c, Participant.Bot("someone"))
            broadcast(leaver, "left the chat!")
            print(f"{leaver.name}: disconnected from the server")
            c.close()
            break


while True:
    client, (ip, port) = server.accept()  # Wait for connections
    participant = pickle.loads(client.recv(1024))  # Receive data from connected client
    print(f"{participant.name} joined from {ip}:{port}")  # Print the information for sys admins

    # So when a client is connected we add the client to a "list" of connected clients. We use dictionary since it is
    # faster to access the items
    clients[client] = participant
    threading.Thread(target=listen_for_data, args=(client,)).start()
    broadcast(participant, f"{participant.name} has joined the chat!")  # Tell everybody who has joined
