# TooGoodToGo Pusher

A small project because it was annoying to never get the good stuff on TooGoodToGo.

This script uses the python tgtg module to get your favorite stores, filter them by availability and send, update and delete info messages via a Telegram bot.

# Installation and Usage

- install requirements by running `pip install -r requirements.txt`
  - usage of venv or similar is recommended
- copy `config.json.example`, rename it to `config.json` and fill it with the needed information of your telegram bot
  - the bot has to be in a group - use the id of the group as chat_id (you can get it from the group URL in Telegram Web)
- run `print_names_of_your_favorites.py` to get a list of the stores in your tgtg favorites
  - the tgtg module will log you in - you will have to click on the link in the log in mail (if on mobile you should copy this link to an incognito tab so you don't get redirected to the tgtg app)
  - the session will be stored locally so you don't have to login every time you execute the script
  - this script will create the `notify_list.json` file - remove an entry from this file if you don't want updates from that store
- run `tgtg_pusher.py`
  - your Telegram bot should now send Messages in the group that should look like this
```txt
Amazing Restaurant
morgen 22:00 - 23:00
    4 verfügbar!
```
