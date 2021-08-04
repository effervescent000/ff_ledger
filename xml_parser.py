import xml.etree.ElementTree as et
import product
import material
from datetime import datetime


class XmlParser:
    def __init__(self, name):
        self.name = name
        self.tree = et.parse(name)
        self.root = self.tree.getroot()
        self.populate_items()

    def add_product_to_xml(self, prod):
        new_prod = et.SubElement(self.root, 'product', {'name': prod.name})
        sales = et.SubElement(new_prod, 'sales', {'sales': prod.sales_str})
        prices = et.SubElement(new_prod, 'price_data')
        for x in prod.price_data:
            et.SubElement(prices, 'price', {'price': x.price_str})
            et.SubElement(prices, 'time', {'time': x.time_str})

    def add_material_to_xml(self, mat):
        new_mat = et.SubElement(self.root, 'material', {'name': mat.name})
        purchases = et.SubElement(new_mat, 'purchases', {'number': mat.purchases_str})
        prices = et.SubElement(new_mat, 'price_data')
        for x in mat.price_data:
            et.SubElement(prices, 'price', {'price': x.price_str})
            et.SubElement(prices, 'time', {'time': x.time_str})

    def populate_items(self):
        for child in self.root:
            if child.tag == 'product':
                self.get_product_from_xml(child)
            elif child.tag == 'material':
                self.get_material_from_xml(child)
            else:
                print('Invalid tag {} passed to populate_items()'.format(child.tag))

    def get_product_from_xml(self, node):
        new_product = product.Product(node.attrib['name'])
        for child in node:
            if child.tag == 'price_data':
                child_price = None
                child_time = None
                for x in child:
                    if x.tag == 'price':
                        child_price = x.attrib['price']
                    else:
                        child.time = x.attrib['time']
                new_product.add_price_point(int(child_price),datetime.strptime(child_time,'%x %X'))

    def get_material_from_xml(self, node):
        new_material = material.Material(node.attrib['name'])
        for child in node:
            if child.tag == 'price_data':
                for price in child:
                    new_material.add_price_point(int(price[0].value), datetime.strptime(price[1].value))

    def save_xml(self):
        print('Saving...')
        self.tree.write(self.name)
