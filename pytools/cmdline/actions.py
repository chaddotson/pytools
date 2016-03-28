from argparse import Action
from datetime import datetime


class DatetimeAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(DatetimeAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

            setattr(namespace, self.dest, datetime.strptime(values, "%Y-%m-%d"))