import time
from tgtg import TgtgClient, TgtgAPIError

from telegram import Telegram
import helpers
import loader


class TgtgPusher:

    def __init__(self, client: TgtgClient, telegram: Telegram):
        self.telegram = telegram
        self.client = client
        self.last_available = {}

    def get_available_stores(self):
        """filter available stores by items in notify_list and by their availability"""
        try:
            favorites = self.client.get_favorites()
        except TgtgAPIError as e:
            print(e)
            return None

        notify_list = loader.load_notify_list()
        available = {}
        for favo in favorites:
            if favo["display_name"] not in notify_list:
                notify_list = loader.update_notify_list(favo["display_name"], True)
            if notify_list[favo["display_name"]] and favo["items_available"]:
                available[favo["display_name"]] = {
                    'count': favo["items_available"],
                    'time_start': helpers.parse_time(favo["pickup_interval"]["start"]),
                    'time_end': helpers.parse_time(favo["pickup_interval"]["end"], no_day=True)
                }
        return available

    def update_last_available(self, available):
        # remove from last_available if not available anymore and delete message
        for store_name in self.last_available.copy():
            if store_name not in available:
                store = self.last_available.pop(store_name)
                store['message'].delete()

        # add to last_available if now available and send/update message
        for store_name, store in available.items():
            message = (f'*{store_name}*\n'
                       f'{store["time_start"]} - {store["time_end"]}\n'
                       f'    {store["count"]} verfügbar!')
            if store_name not in self.last_available:
                self.last_available[store_name] = {
                    'message': self.telegram.send(message),
                    'count': store['count']
                }
            elif self.last_available[store_name]['count'] != store['count']:
                self.last_available[store_name]['message'].edit(message)
                self.last_available[store_name]['count'] = store['count']

    def loop(self):
        while True:
            available = self.get_available_stores()
            if available is None:
                self.telegram.send("can't reach tgtg, trying again in 5 minutes")
                time.sleep(60 * 5)
                continue
            self.update_last_available(available)
            time.sleep(60)

    def start(self):
        try:
            self.loop()
        except Exception as e:
            self.telegram.send(f'something broke! exiting.\n#####\n{e}\n#####')
            raise e


if __name__ == '__main__':

    telegram = loader.load_telegram()
    if telegram is None:
        print('no telegram config found. exiting.')
        exit()
    client = loader.load_tgtg_client()

    # message = telegram.send('test')
    # time.sleep(2)
    # message.edit('test2')
    # time.sleep(2)
    # message.delete()

    pusher = TgtgPusher(client, telegram)
    pusher.start()
