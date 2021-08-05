import tkinter as tk
import gui.new_product_window as npw
import gui.new_material_window as nmw
import material
import product
import xml_parser


class MainWindow:
    def __init__(self, xp):
        self.xp = xp
        self.main_window = tk.Tk()
        self.new_product_window = None

        products = []
        for x in product.product_list:
            products.append(x.name)
        if len(products) == 0:
            products.append('None')

        self.chosen_product = tk.StringVar(self.main_window)
        self.chosen_product.set('Select a product')
        self.product_price_entry = tk.Entry(self.main_window)
        product_menu = tk.OptionMenu(self.main_window, self.chosen_product, *products)
        add_sale_button = tk.Button(self.main_window, text='Add sale')
        edit_entries_products = tk.Button(self.main_window, text='Edit entries')
        add_price_products = tk.Button(self.main_window, text='Add price point')

        add_product_button = tk.Button(self.main_window, text='Add product')

        add_price_products.bind('<Button-1>', self.add_product_price_click)
        add_product_button.bind('<Button-1>', self.add_product_click)

        product_menu.pack()
        self.product_price_entry.pack()
        add_sale_button.pack()
        edit_entries_products.pack()
        add_price_products.pack()
        add_product_button.pack()

        materials = []
        for x in material.material_list:
            materials.append(x.name)
        if len(materials) == 0:
            materials.append('None')

        self.chosen_material = tk.StringVar(self.main_window)
        self.chosen_material.set('Select a material')
        self.material_price_entry = tk.Entry(self.main_window)
        material_menu = tk.OptionMenu(self.main_window, self.chosen_material, *materials)
        add_purchase = tk.Button(self.main_window, text='Add purchase')
        edit_entries_materials = tk.Button(self.main_window, text='Edit entries')
        add_price_materials = tk.Button(self.main_window, text='Add price point')
        add_material_button = tk.Button(self.main_window, text='Add material')

        add_material_button.bind('<Button-1>', self.add_material_click)
        add_price_materials.bind('<Button-1>', self.add_material_price_click)

        save_button = tk.Button(self.main_window, text='Save data')
        load_button = tk.Button(self.main_window, text='Load data')

        save_button.bind('<Button-1>', self.save_button_click)

        material_menu.pack()
        self.material_price_entry.pack()
        add_purchase.pack()
        edit_entries_materials.pack()
        add_price_materials.pack()
        add_material_button.pack()
        save_button.pack()
        load_button.pack()

        self.main_window.mainloop()

    def add_product_price_click(self, event):
        if self.chosen_product is not None and self.product_price_entry.get() is not None:
            prod = product.check_in_products(self.chosen_product.get())
            if prod is not False:
                prod.add_price_point(self.product_price_entry.get())

    def add_material_price_click(self, event):
        if self.chosen_material is not None and self.material_price_entry.get() is not None:
            mat = material.check_in_materials((self.chosen_material.get()))
            if mat is not False:
                mat.add_price_point(self.material_price_entry.get())

    def match_product(self):
        for x in product.product_list:
            if self.chosen_product.get() == x.name:
                return x
        return False

    def match_material(self):
        for x in material.material_list:
            if self.chosen_material.get() == x.name:
                return x
        return False

    def add_material_click(self, event):
        nmw.NewMaterialWindow()

    def add_product_click(self, event):
        npw.NewProductWindow()

    def save_button_click(self, event):
        for x in product.product_list:
            x.prep_for_records()
            self.xp.add_product_to_xml(x)
        for x in material.material_list:
            x.prep_for_records()
            self.xp.add_material_to_xml(x)
        self.xp.save_xml()
