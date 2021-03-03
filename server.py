import socket
import threading

server = socket.socket()
server.bind(("localhost", 4242))
server.listen()

print("Server is running...")

clients = {}


# Define a function that broadcast messages to all the other clients
def broadcast(message):
    for c in clients:
        c.send(message.encode("utf-8"))


def receive_message_from(client):
    while True:  # Tell the server to attempt to retrieve data from the client
        try:
            broadcast(client.recv(1024).decode("utf-8"))  # The program will stay here until data is received
        except:  # If the client is terminated then consider that this client has signed off
            participant = clients.pop(client)  # Remove the client from the list of connected clients
            broadcast(f"{participant} has left the chat!")  # Tell every one else that the participant has left
            break  # Get out of this loop


while True:
    client, address = server.accept()  # When a participant makes a connection
    participant = client.recv(1024).decode("utf-8")  # Broadcast to all the other clients that participant has joined
    broadcast(f"{participant} has joined the chat!")
    print(f"{participant} has joined the server on {address}")  # Inform the server admins about the new participant
    clients[client] = participant  # Add client to dictionary

    # Start listening for any data sent from this client
    threading.Thread(target=receive_message_from, args=(client,)).start()
    # Get back to checking for new connections after starting this thread.
