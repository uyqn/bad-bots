import sys
import Participant
import socket
import pickle
import threading

# Define a dictionary of available bots:
available_bots = {
    'alice': Participant.Alice()
}

# Force user to specify ip and port
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    print("IP and port must be specified. Correct usage e.g $py client.py localhost 2410")
    sys.exit()

# Define the participant:
try:
    participant = \
        available_bots[sys.argv[3].lower()] \
        if len(sys.argv) == 4 \
        else Participant.Person(input("Choose a nickname: "))
except KeyError:
    print(f"Sorry, cannot summon {sys.argv[3]}")
    sys.exit()

# Start the TCP connection:
client = socket.socket()
client.connect((ip, port))

# Send the server about who has connected:
client.send(pickle.dumps(participant))


# So, we want to be able to receive the broadcast message:
def receive_data():
    while True:
        try:
            # We will have the server send back the participant and the message that they sent:
            sender, message = pickle.loads(client.recv(1024))

            # Then we will print the message from the sender:
            print(message)

            # Then we check if the sender is a person or a bot
            if isinstance(participant, Participant.Bot) and isinstance(sender, Participant.Person):
                # If this client is a bot and the sender is a person then we will have the bot respond to the message:
                response = participant.respond_to(sender, message)
                data = pickle.dumps((participant, response))
                client.send(data)
        except:
            print("Server is down!")
            break
    sys.exit()


# We also want to be able to send data. Persons are the only ones able to send messages
def send_data():
    while True:
        data = (participant, input(""))
        client.send(pickle.dumps(data))


# At last we have to start threads to run both functions simultanously:
threading.Thread(target=receive_data).start()

# Since only persons are able to send messages:
if isinstance(participant, Participant.Person):
    threading.Thread(target=send_data).start()
