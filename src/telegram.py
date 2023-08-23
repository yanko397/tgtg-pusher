from message import Message


class Telegram:

    def __init__(self, config: dict):
        self.config = config

    def send(self, text: str) -> Message:
        return Message(self.config, text)
