import re


class Person:
    def __init__(self, name):
        self.name = name


class Bot:
    def __init__(self, name):
        self.name = name

    # We need a method to extract the suggested actions from a message:
    def get_actions(self, message, list_of_actions):
        # Cleanup the message
        message = re.sub("[^A-Za-z]+", " ", message).lower()

        # Create a list of actions (more actions might be suggested in one message)
        actions = list(filter(lambda w: w in list_of_actions, message.split(" ")))
        return actions

    def respond_to(self, participant, message):
        pass


class Alice(Bot):
    ACTIONS = {
        'eat': "Sounds great! I could go for a bite, even though i don't have any digestive systems...",
        'fight': "Violence solves nothing!",
        'study': "It is always great to attain more knowledge :)",
        'sleep': "Sleeping is great for the health.",
        'work': "Work smarter not harder!",
        'play': "All you do is play...",
        'complain': "Sorry, I am not interested in your complains...",
        'hug': "Yes! I love hugs! Hug your screen, let me feel your love!",
        'joined': "Hello there!",
        'left': "See you later alligator!"
    }

    def __init__(self):
        super().__init__('Alice')

    def respond_to(self, participant, message):
        actions = self.get_actions(message, self.ACTIONS)

        if len(actions) == 0:
            return "Sorry! I do not know how to respond to that!"
        else:
            response = ""
            for action in actions:
                response += f"{self.ACTIONS[action]} "
            return response
