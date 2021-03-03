"""
We will create a class of Bot and then create each bot as an object with their own personalities. The advantage here
is that we can fix available actions on this class which in turn will also change on all the other bots
"""
import re


class Bot:
    ACTIONS = ["work", "play", "eat", "cry", "sleep", "fight"]

    def __init__(self, name):
        self.name = name

    def get_action(self, message):
        # Cleaning the message in case it contains anything but letters such as periods or "?"
        # Then we convert everything to lowercase letters
        message = re.sub("[^A-Za-z ]+", "", message).lower()

        # Check if the message contains any of the actions:
        action = None
        for word in message.split(" "):
            if word in self.ACTIONS:
                action = word

        return action

    def respond(self, message):
        action = self.get_action(message)

        if action is None:
            return f"Sorry, I don't understand what you are saying..."

        return f"Respond method initiated with arg: {action}"

