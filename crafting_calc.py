import product


class CraftingCalc:
    def __init__(self):
        pass

    def get_stock(self):
        stock = [x for x in product.product_list if x.stock > 0]
        return stock


