import datetime

import item

product_list = []


def check_in_products(name):
    """
    Checks if an item is in the product_list.
    :param name: String representing the product.
    :return: The product that shares the string (or False if no matching product is found).
    """
    if len(product_list) == 0:
        return False
    else:
        for x in product_list:
            if name == x.name:
                return x
        return False


def add_to_product_list(prod):
    if check_in_products(prod.name) is False:
        product_list.append(prod)
    else:
        print('Attempted to add item {} that is already in product list'.format(prod.name))


class Product(item.Item):
    def __init__(self, name):
        super().__init__(name)
        self.sales = 0
        self.sales_str = None
        self.profit = 0
        self.units = 'gil'  # valid options are 'raw' and 'gph'
        self.stock_data = []
        self.sales_data = []
        self.craftable = True

    def prep_for_records(self):
        """
        Converts certain numeric variables to strings for use in the xml_parser.
        """
        self.price_str = str(self.price)
        if len(self.price_data) > 0:
            for x in self.price_data:
                x.price_str = str(x.price)
                x.time_str = str(x.time)
        self.sales_str = str(self.sales)

    def add_stock(self, time=datetime.datetime.now()):
        """
        Add a single unit of stock to the product, at the time passed (defaults to when the method is called). Also
        prunes old stock records.
        :param time:
        """
        self.stock += 1
        self.stock_data.append(time)
        if len(self.stock_data) > 10:
            self.stock_data.pop(0)

    def add_sale(self, time=datetime.datetime.now()):
        """
        Adds a single sale to the product and subtracts a unit of stack, at the time passed (defaults to when the
        method is called. Also prunes old sale records.
        :param time:
        """
        if self.stock > 0:
            self.stock -= 1
        self.sales += 1
        self.sales_data.append(time)
        if len(self.sales_data) > 10:
            self.sales_data.pop(0)
