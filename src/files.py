import os
import json
from tgtg import TgtgClient

from make_notify_list_json import save_notify_list

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
            json.dump(client.get_credentials(), f, indent=4)
        if not os.path.exists('notify_list.json'):
            save_notify_list()
    return client


def load_notify_list():
    if os.path.exists('notify_list.json'):
        with open('notify_list.json', encoding='utf-8') as f:
            notify_list = json.load(f)
    else:
        notify_list = []
    return notify_list


def load_config():
    if os.path.exists('config.json'):
        with open('config.json', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    return config