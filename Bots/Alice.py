from Bots import Bot


class Alice(Bot.Bot):

    def __init__(self):
        super().__init__("Alice")

    def respond(self, message):
        action = super().get_action(message)
