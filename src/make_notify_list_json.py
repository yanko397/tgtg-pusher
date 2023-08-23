import json

import loader


def save_new_notify_list():
    client = loader.load_tgtg_client()
    notify_list = {favo["display_name"]: True for favo in client.get_favorites()}
    with open('notify_list.json', 'w', encoding='utf-8') as f:
        json.dump(notify_list, f, indent=4, ensure_ascii=False)
    return notify_list


if __name__ == '__main__':
    save_new_notify_list()
