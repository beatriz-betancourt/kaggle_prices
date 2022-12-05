import datetime as dt


class Logger:

    def __init__(self):
        pass

    def print_info(self, msg: str):
        """Log message with date and time"""
        print(f"{dt.date.today()}_{dt.datetime.today().hour}:{dt.datetime.today().minute}::_{msg}")

    def print_size_change(self, ini_len: int, final_len: int, tag: str):
        self.print_info(f"{tag}: Reduce size from {ini_len} to {final_len}")
