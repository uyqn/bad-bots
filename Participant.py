import re
import random
import datetime


class Person:
    def __init__(self, name):
        self.name = name


class Bot:
    ACTIONS = {

    }

    def __init__(self, name):
        self.name = name

    # We need a method to extract the suggested actions from a message:
    def get_actions(self, message):
        # Cleanup the message
        message = re.sub("[^A-Za-z/]+", " ", message).lower()
        self.add_random_actions()

        # Create a list of actions (more actions might be suggested in one message)
        return list(filter(lambda w: w in self.ACTIONS, message.split(" ")))

    def add_random_actions(self):
        pass

    def help(self):
        self.add_random_actions()
        return list(filter(lambda a: a in self.ACTIONS.keys() and a is not None, self.ACTIONS.keys()))

    def respond_to(self, message):
        actions = self.get_actions(message)

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
        "Peek-a-boo! :D"
    ]

    DAY_FACTS = {
        'Monday': "Monday. Did you know that the Latin term for Monday is \"Dies Lunae\", which literally translates "
                  "to \"Day of the Moon\"?",
        'Tuesday': "Tuesday. Did you know that the Greeks consider Tuesday to be an unlucky day as this was the day "
                   "that Constantinople Fell.",
        'Wednesday': "Wednesday. Did you know that in many Slavic languages, Wednesday translates to \"the middle.\"",
        'Thursday': "Thursday. It goes back to Roman times, with the Latin word for Thursday, Iovies Dies, literally "
                    "meaning Jupiter’s Day.",
        'Friday': "Friday. A popular American acronym is \"TGIF,\" which means \"Thank God It’s Friday.\"",
        'Saturday': "Saturday. Did you know that Saturday takes its name from Saturn, the Roman god of generation, "
                    "dissolution, plenty, wealth, agriculture, periodic renewal, and liberation.",
        'Sunday': "Sunday. Did you know that in Slavic languages like Polish, Ukrainian, Croatian, and Bulgarian "
                  "among others, the word for Sunday means \"no work\"."
    }

    JOKES = [
        "What do you call it when computer science majors make fun of each other?\n\tCyber boolean!",
        "My dog ate my computer science project...\n\tIt took him a couple bytes!",
        "I don't like computer science jokes...\n\tNot one bit.",
        "One thing I know is that a computer science major didn't name the original pokemon. "
        "\n\tOtherwise, charmander would evolve into stringmander.",
        "Computer Science major walks into an English class."
        "\n\tThe professor says \"Welcome to English 101\"."
        "\n\tThe student panicks. "
        "\n\t\"What's wrong?\" asks the Professor."
        "\n\t\"I missed the first 4 English classes.\""
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
        'sing': "La-La-La-La"
                "\n\tBa-ba-ri-as-ras-ti-ti-ti-ras-ti-ti"
                "\n\tBa-ba-ri-as-ras-ti-ti-ta"
                "\n\tBa-ba-ri-as-ras-ti-ti-ti-ras-ti-ti"
                "\n\tRastis! Rastis! Ra-ti-ti-la",

        'identify': "It is I, Alice the bot!",
        'who': "My name is Alice, and I am a bot! Beep bop!",

        # Just greetings and farewells when person-clients joins or leaves the server.
        'joined': "Hello there!",
        'left': "See you later alligator!",
        'hello': "Hello back!"
    }

    def __init__(self):
        super().__init__('Alice')

    def add_random_actions(self):
        dt = datetime.datetime.now()
        self.ACTIONS.update({'joke': random.choice(self.JOKES)})
        self.ACTIONS.update({'time': f"{dt.strftime('%X')} "
                                     f"how time flies with such great company!."})
        self.ACTIONS.update({'date': f"Today's date is {dt.strftime('%x')}."})
        self.ACTIONS.update({'day': f"Today is {self.DAY_FACTS[dt.strftime('%A')]}."})
        self.ACTIONS.update({'hi': f"{random.choice(self.GREETINGS)}."})
        self.ACTIONS.update({'hey': f"{random.choice(self.GREETINGS)}."})


class Bob(Bot):
    GREETINGS = [
        "Howdy! :)",
        "What's up homie?!",
        "Yo!",
        "Konichiwa amigo!",
        "Hey? What do you want?"
    ]

    JOKES = [
        "Where do Italian gangsters live? \n\tIn the spaghetto!",
        "What do you call a gangster with clean teeth? \n\t Oral-G!",
        "I heard about the gangster with a weak stomach... \n\t He was throwing up gang signs!",
        "Where do gambling gangsters go after they die? \n\t To the Gangster's-Pair-a-Dice!",
        "Why did the gangster stand under the tree?\n\t Because it was shady!"
    ]

    ACTIONS = {
        # Default response if none of the suggested actions has been programmed
        None: "What bro? Ain't nobody know nothing what you be saying homie!",

        # Actions with responses:
        'eat': "Man, I could go for a bite!",
        'fight': "Ain't nobody be messing with Bob! You wanna go bro?!",
        'study': "Ain't no gangstah that needs to study!",
        'sleep': "Yeah, dog, I could need to hit the bed yo",
        'work': "Plenty of cash, no need to work ;)",
        'play': "I ain't ever playing! Always have your guard up!",
        'complain': "Nah man, can't complain to the boss...",
        'hug': "Maybe I need a hug :(",
        'sing': "Been spendin' most their lives livin' in the gangsta's paradise"
                "\n\tKeep spendin' most our lives livin' in the gangsta's paradise",

        'identify': "Gangster-bot-Bob to ya rescue!",
        'who': "Yo! I'm Bob also known as gangster-bot-Bob!",

        # Just greetings and farewells when person-clients joins or leaves the server.
        'joined': "Yo!",
        'left': "Another goner!",
    }

    def __init__(self):
        super().__init__('Bob')

    def add_random_actions(self):
        self.ACTIONS.update({'joke': random.choice(self.JOKES)})
        self.ACTIONS.update({'time': f"Huh? The clock? It's {datetime.datetime.now().strftime('%X')}."})
        self.ACTIONS.update({'date': f"I got you homie! It's {datetime.datetime.now().strftime('%x')}."})
        self.ACTIONS.update({'day': f"{datetime.datetime.now().strftime('%A')} yo..."})
        self.ACTIONS.update({'hi': f"{random.choice(self.GREETINGS)}."})
        self.ACTIONS.update({'hey': f"{random.choice(self.GREETINGS)}."})
        self.ACTIONS.update({'hello': f"{random.choice(self.GREETINGS)}."})


class Batman(Bot):
    GREETINGS = [
        "Hey..."
    ]

    JOKES = [
        "DO YOU KNOW WHERE JOKER IS?!"
    ]

    ACTIONS = {
        # Default response if none of the suggested actions has been programmed
        None: "I am not obliged to answer you",

        # Actions with responses:
        'eat': "I eat criminals for breakfast!",
        'fight': "We can fight... But you will lose!",
        'study': "If you want to beat your enemies. You have to study them. Know all their habits, all their moves"
                 "\n\t and especially their psychology. That's why Joker is so hard to catch!",
        'sleep': "There is no time for sleep! Botham needs me!",
        'work': "I don't need to work... I am already rich!",
        'play': "I only play with dangerous criminals!",
        'complain': "If you got time to complain, I suggest you spend that time to something else...",
        'hug': "No!",
        'sing': "Na, na, na, na, na, na, na, na, na, na, na, na, na Batman!",

        'identify': "I'm Batman! Wait I'm a bot... I'm BOTMAN!",
        'who': "I'm Batman! Wait, that's not right... I'm Botman protector of Botham!",

        # Just greetings and farewells when person-clients joins or leaves the server.
        'joined': "I see... you came for some action!",
        'left': "Another one bit the dust...",
    }

    def __init__(self):
        super().__init__('Batman')

    def respond_to(self, message):
        actions = self.get_actions(message)

        if len(actions) == 0:
            return self.ACTIONS[None]  # Default response if suggested action has not been programmed
        else:
            response = ""
            for action in actions:
                response += f"{self.ACTIONS[action]} "
                if action == 'who' or action == 'identify':
                    self.ACTIONS.update({'who': "I'm Botman, protector of Botham!"})
                    self.ACTIONS.update({'identify': "I'm Botman!"})
                    self.ACTIONS.update({'sing': "Na, na, na, na, na, na, na, na, na, na, na, na, na Botman!"})
            return response

    def add_random_actions(self):
        self.ACTIONS.update({'joke': random.choice(self.JOKES)})
        self.ACTIONS.update({'time': f"Huh? The clock? It's {datetime.datetime.now().strftime('%X')}."})
        self.ACTIONS.update({'date': f"I got you homie! It's {datetime.datetime.now().strftime('%x')}."})
        self.ACTIONS.update({'day': f"{datetime.datetime.now().strftime('%A')} yo..."})
        self.ACTIONS.update({'hi': f"{random.choice(self.GREETINGS)}."})
        self.ACTIONS.update({'hey': f"{random.choice(self.GREETINGS)}."})
        self.ACTIONS.update({'hello': f"{random.choice(self.GREETINGS)}."})