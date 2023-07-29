import os
import json
import requests
import time
from tgtg import TgtgClient


def telegram_send(message):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/sendMessage'
    try:
        response = requests.post(api_url, json={'chat_id': config["telegram_chat_id"], 'text': str(message)})
        assert response.status_code == 200, f'#####\n{response.text}\n{response.status_code}\n{message}\n#####'
        return response.json()['result']['message_id']
    except Exception as e:
        print(e)


def telegram_delete(message_id):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/deleteMessage'
    try:
        response = requests.post(api_url, json={'chat_id': config["telegram_chat_id"], 'message_id': message_id})
        assert response.status_code == 200, f'#####\n{response.text}\n{response.status_code}\n{message_id}\n#####'
    except Exception as e:
        print(e)


def telegram_edit(message_id, message):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/editMessageText'
    try:
        response = requests.post(api_url, json={'chat_id': config["telegram_chat_id"], 'message_id': message_id, 'text': str(message)})
        assert response.status_code == 200, f'#####\n{response.text}\n{response.status_code}\n{message_id}\n{message}\n#####'
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


def load_notify_list():
    if os.path.exists('notify_list.json'):
        with open('notify_list.json', encoding='utf-8') as f:
            notify_list = json.load(f)
    else:
        notify_list = []
    return notify_list


def main():
    client = load_client()
    notify_list = load_notify_list()
    last_available = {}
    while True:
        available = {}
        for favo in client.get_favorites():
            if favo["display_name"] in notify_list and favo["items_available"]:
                available[favo["display_name"]] = favo["items_available"]

        # remove from last_available if not available anymore and delete message
        for x in last_available.copy():
            if x not in available:
                telegram_delete(last_available.pop(x)['id'])
        # add to last_available if now available and send message
        for x in available:
            message = f'{x}\n    {available[x]} verfügbar!'
            if x not in last_available:
                last_available[x] = {'id': telegram_send(message), 'count': available[x]}
            elif last_available[x]['count'] != available[x]:
                telegram_edit(last_available[x]['id'], message)
                last_available[x]['count'] = available[x]

        time.sleep(60)


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)
    main()
