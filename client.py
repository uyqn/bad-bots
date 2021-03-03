# Importing necessary modules:
import socket  # For TCP connections
import sys  # For command handling commandline parameters
import threading
from Bots import Bot  # Our bots

# Handling exception if too few arguments are passed
"""
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    print("Usage of client.py: $python3 client.py ip port [optional bot]")
    sys.exit()  # Terminating client.py if necessary args has not been passed to the command
"""

participant = sys.argv[1]

# Create a client socket and connect it to the server:
client = socket.socket()
client.connect(("localhost", 4242))
client.send(participant.encode("utf-8"))  # Sending the name of the participant to the server


# Method for receiving broadcasted messages:
def receive_broadcast():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Error occurred closing connection:")
            client.close()
            break


# Method for sending a message:
def send_message():
    while True:
        message = f"{participant}: {input('')}".encode("utf-8")
        client.send(message)


threading.Thread(target=receive_broadcast).start()
threading.Thread(target=send_message).start()
