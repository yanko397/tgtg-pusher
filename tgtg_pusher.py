import os
import json
import pickle
from tgtg import TgtgClient


def load_client():
    if os.path.exists('tgtg_session.pickle'):
        with open('tgtg_session.pickle', 'rb') as f:
            credentials = pickle.load(f)
        client = TgtgClient(
            access_token=credentials['access_token'],
            refresh_token=credentials['refresh_token'],
            user_id=credentials['user_id'],
            cookie=credentials['cookie']
            )
    else:
        client = TgtgClient(email=input('Your email: '))
        with open('tgtg_session.pickle', 'wb') as f:
            pickle.dump(client.get_credentials(), f)
    return client


def main():
    print('Loading client...')
    client = load_client()
    print(client.get_credentials())
    print('Getting favorites...')
    favorites = client.get_favorites()
    print(json.dumps(favorites, indent=2))


if __name__ == '__main__':
    main()
