import Participant

alice = Participant.Alice()

message = "Let's jump around!"
list_of_actions = {None: "Yoyo"}

print(alice.respond_to(message))