from datetime import datetime, timedelta

def parse_time(date_time, no_day=False):
    date_time = datetime.fromisoformat(date_time).astimezone()
    if date_time.date() == datetime.today().date():
        date_time = date_time.strftime('%H:%M')
    elif date_time.date() == datetime.today().date() + timedelta(days=1):
        if no_day:
            date_time = date_time.strftime('%H:%M')
        else:
            date_time = date_time.strftime('morgen %H:%M')
    else:
        date_time = date_time.strftime('%d.%m.%Y %H:%M')
    return date_time