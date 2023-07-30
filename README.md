# TooGoodToGo Pusher

A small project because it was annoying to never get the good stuff on TooGoodToGo.

This script uses the python tgtg module to retrieve your favorite stores. It will then send messages to a specified telegram group, update those messages with the number of available portions or delete them if there are none left.
Messages get updated every minute.

# TLDR

```
git clone https://github.com/yanko397/tgtg-pusher.git
cd tgtg-pusher
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.json.example config.json
# fill config.json with your bot token and chat_id
cd src
python tgtg_pusher.py
# enter email adress, click on link in email you get from tgtg
# remove entries from generated notify_list.json file if you don't want updates for them
```

# Installation and Usage

- install requirements by running `pip install -r requirements.txt`
  - usage of venv or similar is recommended
- copy `config.json.example`, rename it to `config.json` and fill it with the needed information of your telegram bot
  - the bot has to be in a group - use the id of the group as chat_id (you can get it from the group URL in Telegram Web)
- run `python tgtg_pusher.py`
  - the tgtg module will log you in - you will have to click on the link in the login email (if you are on mobile you should copy that link to an incognito tab so you don't get redirected to the tgtg app)
  - the session will be stored in the repo so you don't have to login every time you execute the script
  - a `notify_list.json` file will be created that contains all your saved tgtg favorites - remove an entry from this file if you don't want to get updates from the corresponding store (you can do also do that while the script is running)
  - your Telegram bot should now send messages in the group that look like this
- you can run `python make_notify_list_json.py` to regenerate your `notify_list.json` file
```txt
Amazing Restaurant
morgen 22:00 - 23:00
    4 verfügbar!
```

# TODO

- [ ] add english translations for the messages
- [ ] write a better README
