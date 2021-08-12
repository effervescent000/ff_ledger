import datetime
import price

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


material_list = []


def check_in_materials(name):
    if len(material_list) == 0:
        return False
    else:
        for x in material_list:
            if name == x.name:
                return x
        return False


def add_to_material_list(mat):
    if check_in_materials(mat.name) is False:
        material_list.append(mat)
    else:
        print('Attempted to add item {} that is already in material list'.format(mat.name))


class Item:
    # TODO remove the subclasses of material and product, turn everything into items
    def __init__(self, name):
        self.name = name
        self.price = 0
        self.price_str = None
        self.price_data = []
        self.hq = None  # true or false
        self.reagents = {}
        self.craftable = None  # should be true or false
        self.stock = 0
        self.stock_data = []
        self.sales = 0
        self.sales_data = []
        self.type = None  # valid types are product or material
        self.units = 'gil'

    def add_price_point(self, num, time=datetime.datetime.now()):
        self.price_data.append(price.Price(int(num), time))

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
