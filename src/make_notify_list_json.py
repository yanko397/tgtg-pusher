import json

import files


def get_notify_list():
    client = files.load_client()
    return [favo["display_name"] for favo in client.get_favorites()]


def save_notify_list():
    with open('notify_list.json', 'w', encoding='utf-8') as f:
        json.dump(get_notify_list(), f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    save_notify_list()
