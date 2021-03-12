import sys
import Participant
import socket
import pickle
import threading
import re

# Define a dictionary of available bots:
available_bots = {
    'alice': Participant.Alice(),
    'bob': Participant.Bob(),
    'batman': Participant.Batman(),
    'james': Participant.James(),
    'yoda': Participant.Yoda()
}

# Force user to specify ip and port
try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except (IndexError, ValueError):
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

if isinstance(participant, Participant.Batman):
    who = participant.ACTIONS['who']
    identify = participant.ACTIONS['identify']

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
            if sender.name == "server":
                print(f"{message}")
            elif sender.name != participant.name:
                print(f"{sender.name}: {message}")

            # Then we check if the sender is a person or a bot
            if isinstance(participant, Participant.Bot) and isinstance(sender, Participant.Person):
                # If this client is a bot and the sender is a person then we will have the bot respond to the message:
                response = participant.respond_to(message)
                print(f"{participant.name}: {response}")
                data = pickle.dumps((participant, response))
                client.send(data)

                if isinstance(participant, Participant.Batman) and \
                        (response.__contains__(who) or response.__contains__(identify)):
                    client.send(pickle.dumps((participant, "/update_name Botman")))
                    update_name('Botman')
        except ConnectionResetError:
            print("Server is down!")
            break


# We also want to be able to send data. Persons are the only ones able to send messages
def send_data():
    while True:
        message = re.sub("[ ]+", " ", input().strip())  # clean up the message
        # This function performs a command if the message is a command, and nothing else otherwise
        perform_command(message)
        client.send(pickle.dumps((participant, message)))


# At last we have to start threads to run both functions simultanously:
threading.Thread(target=receive_data).start()

# Since only persons are able to send messages:
if isinstance(participant, Participant.Person):
    threading.Thread(target=send_data).start()


# We also want certain commands to be performed:
def perform_command(message):
    command = message.split(" ")  # create an array of the message
    if command[0] in commands:
        commands[command[0]](" ".join(map(str, command[1:])))


def update_name(new_name):
    old_name = participant.name
    participant.name = new_name
    return old_name


commands = {
    '/update_name': update_name,
}
