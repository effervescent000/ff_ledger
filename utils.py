import datetime
import tkinter as tk

import item

time_format = '%Y-%m-%d %H:%M'


def convert_to_time_format(time):
    """Convert a datetime with too much precision (usually from .now()) to one with less by converting it a string in
    our desired format and back to shear off the seconds"""
    new_time = time.strftime(time_format)
    new_time = datetime.datetime.strptime(new_time, time_format)
    return new_time


def send_warning(warning, text_box=None):
    if text_box is None:
        print(warning)
    else:
        text_box.insert(tk.INSERT, '{}\n'.format(warning))


def get_stock():
    stock = []
    for x in item.product_list:
        if x.stock > 0:
            stock.append((x.stock, x.name))
    return stock
