import material
import product


class CraftingCalc:
    def __init__(self):
        pass

    def get_stock(self):
        stock = []
        for x in product.product_list:
            if x.stock > 0:
                stock.append((x.stock, x.name))
        return stock

    def get_crafting_cost(self, item):
        crafting_cost = 0
        for x in item.reagents.items():
            mat = material.check_in_materials(x[0])
            price = mat.get_price()
            if price == 0:
                print('Material {} missing price data'.format(x[0]))
                return None
            else:
                if len(mat.reagents) > 0:
                    crafting_cost += self.get_crafting_cost(mat) * float(x[1])
                else:
                    crafting_cost += price * float(x[1])
        return crafting_cost

    def get_crafts(self, num):
        """
        Returns a list of items to craft, up to the length of num, preferring ones that have sold before and that are
        not in stock already.

        :param num: The number of items to craft/the length of the list (1-indexed).
        :return: The list of items to craft.
        """
        temp_craft_list = []
        backup_craft_list = []
        craft_list = []
        for x in product.product_list:
            if x.stock <= 0:
                # debug check/message to be removed eventually
                if x.stock < 0:
                    print('{} has < 0 stock'.format(x.name))
                if x.sales > 0:
                    temp_craft_list.append(x)
                else:
                    backup_craft_list.append(x)

        temp_craft_list.sort(key=self.get_profit, reverse=True)
        backup_craft_list.sort(key=self.get_profit, reverse=True)
        if len(temp_craft_list) < num:
            craft_list = [x for x in temp_craft_list]
        else:
            for i in range(num):
                craft_list.append(temp_craft_list[i - 1])
        if len(craft_list) < num:
            print('temp_craft_list too short, adding products without sales')
            for i in range(num - len(craft_list)):
                craft_list.append(backup_craft_list[i])

        return craft_list

    def get_profit(self, item):
        item.profit = item.get_price() - self.get_crafting_cost(item)
        return item.profit
