import os
import json
import requests
import time
from datetime import datetime, timedelta
from tgtg import TgtgClient, TgtgAPIError


def telegram_send(message):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/sendMessage'
    try:
        response = requests.post(api_url, json={
            'chat_id': config["telegram_chat_id"],
            'text': str(message)}
        )
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


def telegram_delete(message_id):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/deleteMessage'
    try:
        response = requests.post(api_url, json={
            'chat_id': config["telegram_chat_id"],
            'message_id': message_id}
        )
        assert response.status_code == 200, (
            f'#####\n'
            f'{response.text}\n'
            f'{response.status_code}\n'
            f'{message_id}\n'
            f'#####'
        )
    except Exception as e:
        print(e)


def telegram_edit(message_id, message):
    api_url = f'https://api.telegram.org/bot{config["telegram_api_token"]}/editMessageText'
    try:
        response = requests.post(api_url, json={
            'chat_id': config["telegram_chat_id"],
            'message_id': message_id,
            'text': str(message)}
        )
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


def parse_time(date_time, no_day=False):
    date_time = datetime.fromisoformat(date_time).astimezone()
    if date_time.date() == datetime.today().date():
        date_time = date_time.strftime('%H:%M')
    elif date_time.date() == datetime.today().date() + timedelta(days=1):
        if no_day:
            date_time = date_time.strftime('%H:%M')
        else:
            date_time = date_time.strftime('morgen %H:%M')
    else:
        date_time = date_time.strftime('%d.%m.%Y %H:%M')
    return date_time


def main():
    client = load_client()
    last_available = {}
    while True:
        # filter available stores by items in notify_list and their availability
        available = {}
        notify_list = load_notify_list()
        try:
            favorites = client.get_favorites()
        except TgtgAPIError as e:
            print(e)
            telegram_send('get_favorites() failed, sleeping for 1 day')
            time.sleep(60 * 60 * 24)
            continue
        for favo in favorites:
            if favo["display_name"] in notify_list and favo["items_available"]:
                available[favo["display_name"]] = {
                    'count': favo["items_available"],
                    'time_start': parse_time(favo["pickup_interval"]["start"]),
                    'time_end': parse_time(favo["pickup_interval"]["end"], no_day=True)
                }

        # remove from last_available if not available anymore and delete message
        for store_name in last_available.copy():
            if store_name not in available:
                store = last_available.pop(store_name)
                telegram_delete(store['message_id'])

        # add to last_available if now available and send/update message
        for store_name, store in available.items():
            message = (f'{store_name}\n'
                       f'{store["time_start"]} - {store["time_end"]}\n'
                       f'    {store["count"]} verfügbar!')
            if store_name not in last_available:
                last_available[store_name] = {
                    'message_id': telegram_send(message),
                    'count': store['count']
                }
            elif last_available[store_name]['count'] != store['count']:
                telegram_edit(last_available[store_name]['message_id'], message)
                last_available[store_name]['count'] = store['count']

        time.sleep(60)


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)
    main()
