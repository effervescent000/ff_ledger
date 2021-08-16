import xml.etree.ElementTree as et
from datetime import datetime

import item

time_format = '%Y-%m-%d %H:%M'


class XmlParser:
    def __init__(self, name):
        self.name = name
        try:
            self.tree = et.parse(name)
            self.root = self.tree.getroot()
            self.populate_items()
        except et.ParseError:
            self.root = et.Element('data')
            self.tree = et.ElementTree(self.root)

    def add_item_to_xml(self, item_obj):
        if self.root.findtext(item_obj.name) is None:
            item_xml = et.SubElement(self.root, item_obj.type)
            item_xml.text = item_obj.name
            stock = et.SubElement(item_xml, 'stock')
            stock.text = str(item_obj.stock)
            if len(item_obj.stock_data) > 0:
                for x in item_obj.stock_data:
                    new_stock = et.SubElement(stock, 'time')
                    new_stock.text = x.strftime(time_format)
            for x in item_obj.price_data:
                price_ele = et.SubElement(item_xml, 'price', {'time': x.time.strftime(time_format)})
                price_ele.text = str(x.price)
            if item_obj.craftable is True:
                et.SubElement(item_xml, 'craftable')
                for x in item_obj.reagents.items():
                    reagent = et.SubElement(item_xml, 'reagent', {'amount': str(x[1])})
                    reagent.text = x[0]

            if item_obj.type == 'product':
                sales = et.SubElement(item_xml, 'sales')
                sales.text = str(item_obj.sales)
                if len(item_obj.sales_data) > 0:
                    for x in item_obj.sales_data:
                        new_sale = et.SubElement(sales, 'time')
                        new_sale.text = x.strftime(time_format)

    def populate_items(self):
        for child in self.root:
            self.get_item_from_xml(child)
        # now that we're done with the tree, delete it. Just nuke it from orbit.
        self.root.clear()
        # TODO figure out how to properly clear the tree to avoid duplicates, leaving this as a todo right now because
        #  I don't think it's breaking anything

    def get_item_from_xml(self, node):
        new_item = item.Item(node.text)
        new_item.type = node.tag
        for child in node.findall('price'):
            if child.text is None:
                child_price = 0
            else:
                child_price = int(child.text)
            child_time = datetime.strptime(child.attrib['time'], time_format)
            new_item.add_price_point(child_price, child_time)

        if new_item.type == 'product':
            sales = node.find('sales')
            if sales is not None:
                new_item.sales = int(sales.text)
                for child in sales:
                    new_item.sales_data.append(datetime.strptime(child.text, time_format))
            stock = node.find('stock')
            if stock is not None:
                new_item.stock = int(stock.text)
                for child in stock:
                    new_item.stock_data.append(datetime.strptime(child.text, time_format))
            item.add_to_product_list(new_item)
            new_item.craftable = True
        elif new_item.type == 'material':
            item.add_to_material_list(new_item)
        else:
            print('Invalid item type {} passed for item {}'.format(new_item.type, new_item.name))

        if new_item.craftable is None:
            if node.find('craftable') is None:
                new_item.craftable = False
            else:
                new_item.craftable = True
        if new_item.craftable is True:
            for child in node.findall('reagent'):
                if child.text is not None:
                    new_item.reagents[child.text] = child.attrib['amount']

    def save_xml(self):
        print('Saving...')
        # first, delete the old file so we aren't just appending to it. Commenting this out b/c I'm not sure this was
        # actually the problem
        with open(self.name, 'w') as f:
            self.tree.write(f, encoding='unicode')
        print('Done saving!')
