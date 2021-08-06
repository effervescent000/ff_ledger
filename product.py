import item

product_list = []


def check_in_products(name):
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

    def prep_for_records(self):
        self.price_str = str(self.price)
        if len(self.price_data) > 0:
            for x in self.price_data:
                x.price_str = str(x.price)
                x.time_str = str(x.time)
        self.sales_str = str(self.sales)
