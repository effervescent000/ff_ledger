import datetime
import math
import tkinter as tk

import item
import utils


class CraftingCalc:
    def __init__(self):
        pass

    def get_stock(self):
        stock = []
        for x in item.product_list:
            if x.stock > 0:
                stock.append((x.stock, x.name))
        return stock

    def get_crafting_cost(self, item_to_check, text_box=None):
        crafting_cost = 0
        for x in item_to_check.reagents.items():
            mat = item.check_in_materials(x[0])
            price = mat.get_price()
            if mat.craftable is False:
                if price == 0:
                    utils.send_warning('Uncraftable material {} missing price data'.format(x[0]), text_box)
                else:
                    crafting_cost += price * float(x[1])
            else:
                if len(mat.reagents) > 0:
                    crafting_cost += self.get_crafting_cost(mat, text_box) * float(x[1])
                else:
                    utils.send_warning('Craftable material {} is missing crafting reagents'.format(x[0]), text_box)
        if 0 < item_to_check.get_price() < crafting_cost and crafting_cost > 0:
            # if it's cheaper to buy an item than craft it, notify the user and use the purchase price as the crafting
            # cost
            utils.send_warning('Item {} is cheaper to buy than craft.'.format(item_to_check.name), text_box)
            crafting_cost = item_to_check.get_price()
        return crafting_cost

    def get_crafts(self, num, text_box=None):
        """
        Returns a list of items to craft, up to the length of num, preferring ones that have sold before and that are
        not in stock already.

        :param text_box: The tkinter text to enter warning messages into
        :param num: The number of items to craft/the length of the list (1-indexed).
        :return: The list of items to craft.
        """
        primary_craft_list = []
        secondary_craft_list = []
        tertiary_craft_list = []
        craft_list = []
        for x in item.product_list:
            if x.stock <= 0:
                # debug check/message to be removed eventually
                if x.stock < 0:
                    print('{} has < 0 stock'.format(x.name))
                if x.sales > 0:
                    gph = self.get_gph(x, text_box)
                    if gph is not None:
                        primary_craft_list.append(x)
                        x.profit = gph
                        x.units = 'gph'
                    else:
                        secondary_craft_list.append(x)
                        x.profit = self.get_profit(x, text_box)
                else:
                    tertiary_craft_list.append(x)
                    x.profit = self.get_profit(x, text_box)

        primary_craft_list.sort(key=self.get_gph, reverse=True)
        secondary_craft_list.sort(key=self.get_profit, reverse=True)
        tertiary_craft_list.sort(key=self.get_profit, reverse=True)

        if len(primary_craft_list) < num:
            craft_list = [x for x in primary_craft_list]
        else:
            for i in range(num):
                craft_list.append(primary_craft_list[i])

        if len(craft_list) < num:
            print('primary_craft_list too short, adding products without gph calculation but with sales')
            n = num - len(craft_list)
            if n < len(secondary_craft_list):
                for i in range(num - len(craft_list)):
                    craft_list.append(secondary_craft_list[i])
            else:
                for i in range(len(secondary_craft_list)):
                    craft_list.append(secondary_craft_list[i])

        if len(craft_list) < num:
            print('secondary_craft_list too short, adding products without sales')
            n = num - len(craft_list)
            if n < len(tertiary_craft_list):
                for i in range(num - len(craft_list)):
                    craft_list.append(tertiary_craft_list[i])
            else:
                for i in range(len(tertiary_craft_list)):
                    craft_list.append(tertiary_craft_list[i])

        return craft_list

    def get_profit(self, item_arg, text_box=None):
        return item_arg.get_price() - self.get_crafting_cost(item_arg, text_box)

    def get_gph(self, item_arg, text_box=None):
        """
        Derive gil/hour.
        """
        if len(item_arg.sales_data) > 0 and len(item_arg.stock_data) > 0:
            # figure out the average time between stocking and selling
            deltas = []
            copy_stock_data = [x for x in item_arg.stock_data]
            for x in item_arg.sales_data:
                matching_stock = self.match_stock(x, copy_stock_data)
                if matching_stock is not None:
                    deltas.append(x - matching_stock)
                    copy_stock_data.remove(matching_stock)
            total_time = datetime.timedelta()
            if len(deltas) > 0:
                for x in deltas:
                    total_time += x
                avg_time = total_time / len(deltas)
                return math.floor(self.get_profit(item_arg, text_box) / (avg_time.days * 24 + avg_time.seconds / 3600))

    def match_stock(self, sale_time, stock_list):
        for x in stock_list:
            if x < sale_time:
                # disregard matches that have a time gap of longer than a week
                time_gap = sale_time - x
                # TODO add an option for setting the desired time gap
                if time_gap.days < 7:
                    return x
