import material
import product


class CraftingCalc:
    def __init__(self):
        pass

    def get_stock(self):
        stock = [x for x in product.product_list if x.stock > 0]
        return stock

    def drill_down(self, item):
        crafting_cost = 0
        for x in item.reagents.items():
            mat = material.check_in_materials(x[0])
            price = mat.get_price()
            if price == 0:
                print('Material {} missing price data'.format(x[0]))
                return None
            else:
                if len(mat.reagents) > 0:
                    crafting_cost += self.drill_down(mat) * float(x[1])
                else:
                    crafting_cost += price * float(x[1])
        return crafting_cost
