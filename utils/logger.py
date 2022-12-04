import datetime as dt


class Logger:

    def __init__(self):

        pass

    def print_info(self, msg: str):
        """Log message with date and time"""
        print(f"{dt.date.today()}_{dt.time.hour}: {dt.time.minute}_{msg}")