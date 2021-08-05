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
        sales = et.SubElement(new_prod, 'sales')
        sales.text = str(prod.sales)
        for x in prod.price_data:
            price_element = et.SubElement(new_prod, 'price', {'time': x.time_str})
            price_element.text = str(x.price)

    def add_material_to_xml(self, mat):
        new_mat = et.SubElement(self.root, 'material', {'name': mat.name})
        purchases = et.SubElement(new_mat, 'purchases')
        purchases.text = str(mat.purchases)
        for x in mat.price_data:
            price_element = et.SubElement(new_mat, 'price', {'time': x.time_str})
            price_element.text = str(x.price)

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
            if child.tag == 'price':
                child_price = int(child.text)
                child_time = datetime.strptime(child.attrib['time'], '%Y-%m-%d %H:%M:%S.%f')
                new_product.add_price_point(child_price, child_time)
        product.add_to_product_list(new_product)

    def get_material_from_xml(self, node):
        new_material = material.Material(node.attrib['name'])
        for child in node:
            if child.tag == 'price':
                child_price = int(child.text)
                child_time = datetime.strptime(child.attrib['time'], '%Y-%m-%d %H:%M:%S.%f')
                new_material.add_price_point(child_price, child_time)
        material.add_to_material_list(new_material)

    def save_xml(self):
        print('Saving...')
        self.tree.write(self.name)
        print('Done saving!')
