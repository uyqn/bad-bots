import re
import random
import datetime


class Person:
    def __init__(self, name):
        self.name = name


class Bot:
    ACTIONS = {}

    def __init__(self, name):
        self.name = name

    # We need a method to extract the suggested actions from a message:
    def __get_actions(self, message):
        # Cleanup the message
        message = re.sub("[^A-Za-z]+", " ", message).lower()

        # Create a list of actions (more actions might be suggested in one message)
        return list(filter(lambda w: w in self.ACTIONS, message.split(" ")))

    def respond_to(self, message):
        actions = self.__get_actions(message)

        if len(actions) == 0:
            return self.ACTIONS[None]  # Default response if suggested action has not been programmed
        else:
            response = ""
            for action in actions:
                response += f"{self.ACTIONS[action]} "
            return response


class Alice(Bot):
    GREETINGS = [
        "Good day to you! :)",
        "I greet thee who greet me!",
        "Yo!",
    ]

    JOKES = [
        "What do you call it when computer science majors make fun of each other?\nCyber boolean!",
        "My dog ate my computer science project...\nIt took him a couple bytes!",
        "I don't like computer science jokes...\nNot one bit."
        "One thing I know is that a computer science major didn't name the original pokemon. "
        "\nOtherwise, charmander would evolve into stringmander.",
        "Computer Science major walks into an English class.\nThe professor says \"Welcome to English 101\"."
        "\nThe student panicks. \"What's wrong?\" asks the Professor.\n\"I missed the first 4 English classes.\""
    ]

    ACTIONS = {
        # Default response if none of the suggested actions has been programmed
        None: "Sorry! I am not programmed to respond to that... :(",

        # Actions with responses:
        'eat': "Sounds great! I could go for a bite, even though i don't have any digestive systems...",
        'fight': "Violence solves nothing!",
        'study': "It is always great to attain more knowledge :)",
        'sleep': "Sleeping is great for the health.",
        'work': "Work smarter not harder!",
        'play': "All you do is play...",
        'complain': "Sorry, I am not interested in your complains...",
        'hug': "Yes! I love hugs! Hug your screen, let me feel your love!",
        'joke': random.choice(JOKES),

        'identify': "It is I, Alice the bot!",
        'who': "My name is Alice, and I am a bot! Beep bop!",

        'time': f"It is currently {datetime.datetime.now().strftime('%X')}.",
        'date': f"Today's date is {datetime.datetime.now().strftime('%x')}",
        'day': f"Today is {datetime.datetime.now().strftime('%A')}.",

        # Just greetings and farewells when person-clients joins or leaves the server.
        'joined': "Hello there!",
        'left': "See you later alligator!",
        'hi': random.choice(GREETINGS),
        'hey': random.choice(GREETINGS),
        'hello': "Hello back!"
    }

    def __init__(self):
        super().__init__('Alice')
