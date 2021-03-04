# DATA2410: Portfolio assignment 1: Bad bots
This assignment is 1/2 assignments that will count toward the final grade of the subject DATA2410 that is taught 
at OsloMet. The goal of this assignment is to create a chatroom by creating a server. Then, clients can connect to the
server and start chatting with each other. This implementation is supposed to run on a single computer. The clients
runs on multiple terminal windows to simulate various participants.

To start the server with specified ip and port:\
$python3 server.py <u>ip</u> <u>port</u>

To start a client that should connect to specified ip and port:\
$python3 client.py <u>ip</u> <u>port</u> [ <u>bot_name</u> ]
> -b <u>bot_name</u>: specify the bot you want this client to be from the list of available bots
>> Current available bots: Alice, Bob, Eve

> Example usage (connecting as a person to localhost:2410):\
>> $python3 client.py localhost 2410

> Example usage (connecting as a bot (Alice) to localhost:2410):
>> $python3 client.py localhost 2410 alice

## Task 1: TCP client