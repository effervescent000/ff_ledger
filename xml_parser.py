import xml.etree.ElementTree as et
from datetime import datetime

import item


class XmlParser:
    def __init__(self, name):
        self.name = name
        self.time_format = '%Y-%m-%d %H:%M:%S.%f'
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
            stock.text = item_obj.stock
            if len(item_obj.stock_data) > 0:
                for x in item_obj.stock_data:
                    new_stock = et.SubElement(stock, 'time')
                    new_stock.text = str(x)
            for x in item_obj.price_data:
                price_ele = et.SubElement(item_xml, 'price', {'time': x.time_str})
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
                        new_sale.text = str(x)

    # def add_product_to_xml(self, prod):
    #     # TODO add HQ as an attribute
    #     if self.root.findtext(prod.name) is None:
    #         new_prod = et.SubElement(self.root, 'product')
    #         new_prod.text = prod.name
    #         sales = et.SubElement(new_prod, 'sales')
    #         sales.text = str(prod.sales)
    #         if len(prod.sales_data) > 0:
    #             for x in prod.sales_data:
    #                 new_sale = et.SubElement(sales, 'time')
    #                 new_sale.text = str(x)
    #         stock = et.SubElement(new_prod, 'stock')
    #         stock.text = str(prod.stock)
    #         if len(prod.stock_data) > 0:
    #             for x in prod.stock_data:
    #                 new_stock = et.SubElement(stock, 'time')
    #                 new_stock.text = str(x)
    #         for x in prod.price_data:
    #             price_element = et.SubElement(new_prod, 'price', {'time': x.time_str})
    #             price_element.text = str(x.price)
    #         for x in prod.reagents.items():
    #             reagent = et.SubElement(new_prod, 'reagent', {'amount': str(x[1])})
    #             reagent.text = x[0]
    #
    # def add_material_to_xml(self, mat):
    #     # TODO add HQ as an attribute
    #     if self.root.findtext(mat.name) is None:
    #         new_mat = et.SubElement(self.root, 'material')
    #         new_mat.text = mat.name
    #         purchases = et.SubElement(new_mat, 'purchases')
    #         purchases.text = str(mat.purchases)
    #         for x in mat.price_data:
    #             price_element = et.SubElement(new_mat, 'price', {'time': x.time_str})
    #             price_element.text = str(x.price)
    #         for x in mat.reagents.items():
    #             reagent = et.SubElement(new_mat, 'reagent', {'amount': str(x[1])})
    #             reagent.text = x[0]
    #         if mat.craftable is True:
    #             # add an empty craftable tag if the item can be crafted, the absence of this tag means craftable = False
    #             et.SubElement(new_mat, 'craftable')

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
            child_time = datetime.strptime(child.attrib['time'], self.time_format)
            new_item.add_price_point(child_price, child_time)

        if new_item.type == 'product':
            sales = node.find('sales')
            if sales is not None:
                new_item.sales = int(sales.text)
                for child in sales:
                    new_item.sales_data.append(datetime.strptime(child.text, self.time_format))
            stock = node.find('stock')
            if stock is not None:
                new_item.stock = int(stock.text)
                for child in stock:
                    new_item.stock_data.append(datetime.strptime(child.text, self.time_format))
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

    # def get_product_from_xml(self, node):
    #     new_product = product.Product(node.text)
    #     for child in node.findall('price'):
    #         if child.text is None:
    #             child_price = 0
    #         else:
    #             child_price = int(child.text)
    #         child_time = datetime.strptime(child.attrib['time'], self.time_format)
    #         new_product.add_price_point(child_price, child_time)
    #     for child in node.findall('reagent'):
    #         if child.text is not None:
    #             new_product.reagents[child.text] = child.attrib['amount']
    #     product.add_to_product_list(new_product)
    #     sales = node.find('sales')
    #     if sales is not None:
    #         new_product.sales = int(sales.text)
    #         for child in sales:
    #             new_product.sales_data.append(datetime.strptime(child.text, self.time_format))
    #     stock = node.find('stock')
    #     if stock is not None:
    #         new_product.stock = int(stock.text)
    #         for child in stock:
    #             new_product.stock_data.append(datetime.strptime(child.text, self.time_format))

    # def get_material_from_xml(self, node):
    #     new_material = material.Material(node.text)
    #     for child in node.findall('price'):
    #         if child.text is None:
    #             child_price = 0
    #         else:
    #             child_price = int(child.text)
    #         child_time = datetime.strptime(child.attrib['time'], self.time_format)
    #         new_material.add_price_point(child_price, child_time)
    #     for child in node.findall('reagent'):
    #         if child.text is not None:
    #             new_material.reagents[child.text] = child.attrib['amount']
    #     material.add_to_material_list(new_material)
    #     if node.find('craftable') is None:
    #         new_material.craftable = False
    #     else:
    #         new_material.craftable = True

    def save_xml(self):
        print('Saving...')
        # first, delete the old file so we aren't just appending to it. Commenting this out b/c I'm not sure this was
        # actually the problem
        with open(self.name, 'w') as f:
            self.tree.write(f, encoding='unicode')
        print('Done saving!')
