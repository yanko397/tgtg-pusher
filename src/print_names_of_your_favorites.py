import json

import files


client = files.load_client()

favorites = []
for favo in client.get_favorites():
    favorites.append(favo["display_name"])

with open('notify_list.json', 'w', encoding='utf-8') as f:
    json.dump(favorites, f, indent=4, ensure_ascii=False)
