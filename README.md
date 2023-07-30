# TooGoodToGo Pusher

A small project because it was annoying to never get the good stuff on TooGoodToGo.

This script uses the python tgtg module to get your favorite stores, filter them by availability and send, update and delete info messages via a Telegram bot.

# TLDR

```
git clone https://github.com/yanko397/tgtg-pusher.git
cd tgtg-pusher
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.json.example config.json
# fill config.json with your bot token and chat_id
python print_names_of_your_favorites.py
# enter email adress, click on link in email you get from tgtg
# remove entries from generated notify_list.json file if you don't want updates
python tgtg_pusher.py
```

# Installation and Usage

- install requirements by running `pip install -r requirements.txt`
  - usage of venv or similar is recommended
- copy `config.json.example`, rename it to `config.json` and fill it with the needed information of your telegram bot
  - the bot has to be in a group - use the id of the group as chat_id (you can get it from the group URL in Telegram Web)
- run `print_names_of_your_favorites.py` to get a list of the stores in your tgtg favorites
  - the tgtg module will log you in - you will have to click on the link in the login email (if you are on mobile you should copy that link to an incognito tab so you don't get redirected to the tgtg app)
  - the session will be stored in the repo so you don't have to login every time you execute the script
  - this script will create the `notify_list.json` file - remove an entry from this file if you don't want updates from the corresponding store
- run `tgtg_pusher.py`
  - your Telegram bot should now send Messages in the group that look like this
```txt
Amazing Restaurant
morgen 22:00 - 23:00
    4 verfügbar!
```

# TODO

- [ ] add english translations for the messages
- [ ] write a better README
