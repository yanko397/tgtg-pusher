import time
from tgtg import TgtgAPIError

from telegram import Telegram
import helpers
import files


class TgtgPusher:

    def __init__(self):
        self.telegram = Telegram(files.load_config())
        self.client = files.load_client()
        self.last_available = {}

    def get_available_stores(self):
        """filter available stores by items in notify_list and by their availability"""
        try:
            favorites = self.client.get_favorites()
        except TgtgAPIError as e:
            print(e)
            return None

        notify_list = files.load_notify_list()
        available = {}
        for favo in favorites:
            if favo["display_name"] in notify_list and favo["items_available"]:
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
                self.telegram.delete(store['message_id'])

        # add to last_available if now available and send/update message
        for store_name, store in available.items():
            message = (f'*{store_name}*\n'
                       f'{store["time_start"]} - {store["time_end"]}\n'
                       f'    {store["count"]} verfügbar!')
            if store_name not in self.last_available:
                self.last_available[store_name] = {
                    'message_id': self.telegram.send(message),
                    'count': store['count']
                }
            elif self.last_available[store_name]['count'] != store['count']:
                self.telegram.edit(self.last_available[store_name]['message_id'], message)
                self.last_available[store_name]['count'] = store['count']

    def loop(self):
        while True:
            available = self.get_available_stores()
            if available is None:
                self.telegram.send('potentially banned from tgtg, sleeping for 1 day')
                time.sleep(60 * 60 * 24)
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
    pusher = TgtgPusher()
    pusher.start()

