from message import Message


class SimpleTelegram:

    def __init__(self, config: dict):
        self.config = config

    def send(self, text: str) -> Message:
        return Message(self.config, text)
