import os
import json
import requests
from tgtg import TgtgClient


def send_to_telegram(message):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/sendMessage'
    try:
        requests.post(api_url, json={'chat_id': config["telegram_chat_id"], 'text': str(message)})
    except Exception as e:
        print(e)


def load_client():
    if os.path.exists('tgtg_session.json'):
        with open('tgtg_session.json') as f:
            credentials = json.load(f)
        client = TgtgClient(
            access_token=credentials['access_token'],
            refresh_token=credentials['refresh_token'],
            user_id=credentials['user_id'],
            cookie=credentials['cookie']
            )
    else:
        client = TgtgClient(email=input('Your email: '))
        with open('tgtg_session.json', 'w') as f:
            json.dump(client.get_credentials(), f)
    return client


def main():
    client = load_client()
    favorites = client.get_favorites()
    favo_list = []
    for favo in favorites:
        favo_list.append({
            'name': favo["store"]["store_name"],
            'available': favo["items_available"]
            })
    send_to_telegram(favo_list)


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)
    main()
