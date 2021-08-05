import datetime
import statistics

import price


class Item:
    def __init__(self, name):
        self.name = name
        self.price = 0
        self.price_str = None
        self.price_data = []
        self.hq = None # true or false
        self.reagents = {}
        self.craftable = None  # should be true or false

    def add_price_point(self, num, time=datetime.datetime.now()):
        self.price_data.append(price.Price(num, time))

    def get_price(self):
        price_list = [x.price for x in self.price_data if x.price > 0]
        if len(price_list) > 0:
            self.price = sum(price_list) / len(price_list)
        else:
            self.price = 0
        return self.price

    def prep_for_records(self):
        self.price_str = str(self.price)
        if len(self.price_data) > 0:
            for x in self.price_data:
                x.price_str = str(x.price)
                x.time_str = str(x.time)
