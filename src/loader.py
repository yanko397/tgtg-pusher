import os
import json
from tgtg import TgtgClient

from make_notify_list_json import save_new_notify_list
from telegram import Telegram

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sessionfile = 'tgtg_session.json'
notify_list_file = 'notify_list.json'
telegram_config_file = 'config.json'


def load_tgtg_client() -> TgtgClient:
    if os.path.exists(sessionfile):
        with open(sessionfile) as f:
            credentials = json.load(f)
        client = TgtgClient(
            access_token=credentials['access_token'],
            refresh_token=credentials['refresh_token'],
            user_id=credentials['user_id'],
            cookie=credentials['cookie']
        )
    else:
        client = TgtgClient(email=input('Your email: '))
        with open(sessionfile, 'w') as f:
            json.dump(client.get_credentials(), f, indent=4)
        if not os.path.exists(notify_list_file):
            save_new_notify_list()
    return client


def load_notify_list() -> dict:
    if os.path.exists(notify_list_file):
        with open(notify_list_file, encoding='utf-8') as f:
            notify_list = json.load(f)
    else:
        notify_list = save_new_notify_list()
    return notify_list


def update_notify_list(store_name: str, value: bool) -> dict:
    notify_list = load_notify_list()
    notify_list[store_name] = value
    with open(notify_list_file, 'w', encoding='utf-8') as f:
        json.dump(notify_list, f, indent=4, ensure_ascii=False)
    return notify_list


def load_telegram() -> Telegram:
    if os.path.exists(telegram_config_file):
        with open(telegram_config_file, encoding='utf-8') as f:
            return Telegram(json.load(f))
    else:
        return None