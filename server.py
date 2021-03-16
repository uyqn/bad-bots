import pickle
import socket
import sys
import threading
import Participant

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
            if not perform_command(c, message) and len(message) > 0:
                broadcast(sender, message)

        except (ConnectionResetError, EOFError):
            leaver = clients.pop(c, Participant.Person("someone"))
            broadcast(Participant.Bot("server"), f"{leaver.name} left the chat!")
            print(f"{leaver.name} disconnected from the server")
            break
        except OSError:
            if len(clients) == 0:
                server.close()
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


def send_help(client, arg):
    available_commands = list(commands.keys())
    available_commands.append("/logout")

    help_message = f"These are the following available commands:\n{available_commands}"
    for c in clients:
        if isinstance(clients[c], Participant.Bot):
            help_message += f"\n{clients[c].name} " \
                            f"responds to any sentences that includes one or more of thse keywords:" \
                            f"\n{clients[c].get_help()}"

    package = pickle.dumps((Participant.Bot("server"), help_message))
    client.send(package)


def kick(client, participant):
    to_be_kicked = None
    for c in clients:
        if clients[c].name.lower() == participant.lower():
            broadcast(Participant.Bot("server"),
                      f"{clients[c].name} has been kicked by {clients[client].name}")
            to_be_kicked = c
    if isinstance(to_be_kicked, socket.socket):
        clients.pop(to_be_kicked)
        to_be_kicked.close()


def shutdown(client, arg):
    broadcast(Participant.Bot("server"), f"{clients[client].name} is shutting down the server")
    for c in clients:
        c.close()
    clients.clear()
    server.shutdown(socket.SHUT_RDWR)


commands = {
    '/update_name': update_name,
    '/help': send_help,
    '/kick': kick,
    '/shutdown_server': shutdown
}

while True:
    try:
        client, (ip, port) = server.accept()  # Wait for connections
    except OSError:
        server.close()
        break
    participant = pickle.loads(client.recv(1024))  # Receive data from connected client
    print(f"{participant.name} joined from {ip}:{port}")  # Print the information for sys admins

    # So when a client is connected we add the client to a "list" of connected clients. We use dictionary since it is
    # faster to access the items
    clients.update({client: participant})
    threading.Thread(target=listen_for_data, args=(client,)).start()
    broadcast(Participant.Person("server"), f"{participant.name} has joined the chat!")  # Tell everybody who has joined
