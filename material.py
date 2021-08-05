import item

material_list = []


def check_in_materials(name):
    if len(material_list) == 0:
        return False
    else:
        for x in material_list:
            if name == x.name:
                return x
            else:
                return False


def add_to_material_list(mat):
    if check_in_materials(mat.name) is False:
        material_list.append(mat)
    else:
        print('Attempted to add item {} that is already in material list'.format(mat.name))


class Material(item.Item):
    def __init__(self, name):
        # TODO include the cost to craft, buy on AH, or buy from vendor and choose the cheapest option
        super().__init__(name)
        # TODO figure out best way to organize purchases
        self.purchases = 0
        self.purchases_str = None

    def prep_for_records(self):
        self.price_str = str(self.price)
        if len(self.price_data) > 0:
            for x in self.price_data:
                x.price_str = str(x.price)
                x.time_str = str(x.time)
        self.purchases_str = str(self.purchases)
