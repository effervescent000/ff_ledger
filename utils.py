import datetime

time_format = '%Y-%m-%d %H:%M'


def convert_to_time_format(time):
    """Convert a datetime with too much precision (usually from .now()) to one with less by converting it a string in
    our desired format and back to shear off the seconds"""
    new_time = time.strftime(time_format)
    new_time = datetime.datetime.strptime(new_time, time_format)
    return new_time
