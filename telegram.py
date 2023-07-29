import requests


class Telegram:

    def __init__(self, config):
        self.config = config

    def send(self, message):
        api_url = f'https://api.telegram.org/bot{self.config["telegram_api_token"]}/sendMessage'
        try:
            response = requests.post(api_url, json={
                'chat_id': self.config["telegram_chat_id"],
                'text': str(message),
                'parse_mode': 'Markdown'
            })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{message}\n'
                f'#####'
            )
            return response.json()['result']['message_id']
        except Exception as e:
            print(e)

    def delete(self, message_id):
        api_url = f'https://api.telegram.org/bot{self.config["telegram_api_token"]}/deleteMessage'
        try:
            response = requests.post(api_url, json={
                'chat_id': self.config["telegram_chat_id"],
                'message_id': message_id
            })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{message_id}\n'
                f'#####'
            )
        except Exception as e:
            print(e)

    def edit(self, message_id, message):
        api_url = f'https://api.telegram.org/bot{self.config["telegram_api_token"]}/editMessageText'
        try:
            response = requests.post(api_url, json={
                'chat_id': self.config["telegram_chat_id"],
                'message_id': message_id,
                'text': str(message),
                'parse_mode': 'Markdown'
            })
            assert response.status_code == 200, (
                f'#####\n'
                f'{response.text}\n'
                f'{response.status_code}\n'
                f'{message}\n'
                f'{message_id}\n'
                f'#####'
            )
        except Exception as e:
            print(e)
