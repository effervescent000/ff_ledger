import xml.etree.ElementTree as et
import product
import material
from datetime import datetime


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

    def add_product_to_xml(self, prod):
        # TODO add HQ as an attribute
        if self.root.findtext(prod.name) is None:
            new_prod = et.SubElement(self.root, 'product')
            new_prod.text = prod.name
            sales = et.SubElement(new_prod, 'sales')
            sales.text = str(prod.sales)
            for x in prod.price_data:
                price_element = et.SubElement(new_prod, 'price', {'time': x.time_str})
                price_element.text = str(x.price)
            for x in prod.reagents.items():
                reagent = et.SubElement(new_prod, 'reagent', {'amount': str(x[1])})
                reagent.text = x[0].name

    def add_material_to_xml(self, mat):
        # TODO add HQ as an attribute
        if self.root.findtext(mat.name) is None:
            new_mat = et.SubElement(self.root, 'material')
            new_mat.text = mat.name
            purchases = et.SubElement(new_mat, 'purchases')
            purchases.text = str(mat.purchases)
            for x in mat.price_data:
                price_element = et.SubElement(new_mat, 'price', {'time': x.time_str})
                price_element.text = str(x.price)
            for x in mat.reagents.items():
                reagent = et.SubElement(new_mat, 'reagent', {'amount': str(x[1])})
                reagent.text = x[0].name

    def populate_items(self):
        for child in self.root:
            if child.tag == 'product':
                self.get_product_from_xml(child)
            elif child.tag == 'material':
                self.get_material_from_xml(child)
            else:
                print('Invalid tag {} passed to populate_items()'.format(child.tag))
        # now that we're done with the tree, delete it. Just nuke it from orbit.
        self.root.clear()
        # TODO figure out how to properly clear the tree to avoid duplicates, leaving this as a todo right now because
        #  I don't think it's breaking anything

    def get_product_from_xml(self, node):
        new_product = product.Product(node.text)
        for child in node.findall('price'):
            if child.text is None:
                child_price = 0
            else:
                child_price = int(child.text)
            child_time = datetime.strptime(child.attrib['time'], '%Y-%m-%d %H:%M:%S.%f')
            new_product.add_price_point(child_price, child_time)
        for child in node.findall('reagent'):
            if child.text is not None:
                check_child = material.check_in_materials(child.text)
                if check_child is not False:
                    new_product.reagents[check_child] = child.attrib['amount']
                else:
                    new_reagent = material.Material(child.text)
                    new_product.reagents[new_reagent] = child.attrib['amount']
        product.add_to_product_list(new_product)

    def get_material_from_xml(self, node):
        new_material = material.Material(node.text)
        for child in node.findall('price'):
            if child.text is None:
                child_price = 0
            else:
                child_price = int(child.text)
            child_time = datetime.strptime(child.attrib['time'], '%Y-%m-%d %H:%M:%S.%f')
            new_material.add_price_point(child_price, child_time)
        for child in node.findall('reagent'):
            if child.text is not None:
                check_child = material.check_in_materials(child.text)
                if check_child is not False:
                    new_material.reagents[check_child] = child.attrib['amount']
                else:
                    new_reagent = material.Material(child.text)
                    new_material.reagents[new_reagent] = child.attrib['amount']
        material.add_to_material_list(new_material)

    def save_xml(self):
        print('Saving...')
        # first, delete the old file so we aren't just appending to it. Commenting this out b/c I'm not sure this was
        # actually the problem
        with open(self.name, 'w') as f:
            self.tree.write(f, encoding='unicode')
        print('Done saving!')
