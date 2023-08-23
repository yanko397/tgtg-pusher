import requests

class Message:

    def __init__(self, config: dict, text: str):
        self.text = text
        self.config = config
        api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/sendMessage'
        try:
            response = requests.post(api_url, json={
                'chat_id': config["telegram_chat_id"],
                'text': str(text),
                'parse_mode': 'Markdown'
                })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{text}\n'
                f'#####'
                )
            self.message_id = response.json()['result']['message_id']
        except Exception as e:
            print(e)

    def __eq__(self, __value: object) -> bool:
        return self.text == __value

    def __str__(self) -> str:
        return self.text

    def edit(self, text: str):
        api_url = f'https://api.telegram.org/bot{self.config["telegram_api_token"]}/editMessageText'
        try:
            response = requests.post(api_url, json={
                'chat_id': self.config["telegram_chat_id"],
                'message_id': self.message_id,
                'text': text,
                'parse_mode': 'Markdown'
                })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{text}\n'
                f'{self.message_id}\n'
                f'#####'
                )
        except Exception as e:
            print(e)

    def delete(self):
        api_url = f'https://api.telegram.org/bot{self.config["telegram_api_token"]}/deleteMessage'
        try:
            response = requests.post(api_url, json={
                'chat_id': self.config["telegram_chat_id"],
                'message_id': self.message_id
                })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{self.message_id}\n'
                f'#####'
                )
        except Exception as e:
            print(e)
