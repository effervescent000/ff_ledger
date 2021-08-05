import tkinter as tk

import gui.new_material_window as nmw
import gui.new_product_window as npw
import material
import product


class MainWindow:
    def __init__(self, xp):
        self.xp = xp
        self.main_window = tk.Tk()

        self.products = []
        for x in product.product_list:
            self.products.append(x.name)
        if len(self.products) == 0:
            self.products.append('None')

        # TODO figure out how to get the optionmenus to update without having to restart the application

        self.chosen_product = tk.StringVar(self.main_window)
        self.chosen_product.set('Select a product')
        self.product_price_entry = tk.Entry(self.main_window)
        self.product_menu = tk.OptionMenu(self.main_window, self.chosen_product, *self.products)
        add_sale_button = tk.Button(self.main_window, text='Add sale')
        edit_entries_products = tk.Button(self.main_window, text='Edit entries')
        add_price_products = tk.Button(self.main_window, text='Add price point')

        add_product_button = tk.Button(self.main_window, text='Add product')

        add_price_products.bind('<Button-1>', self.add_product_price_click)
        add_sale_button.bind('<Button-1>', self.add_sale_click)
        add_product_button.bind('<Button-1>', self.add_product_click)

        self.product_menu.grid(row=0, column=0)
        self.product_price_entry.grid(row=0, column=1)
        add_sale_button.grid(row=0, column=2)
        edit_entries_products.grid(row=0, column=3)
        add_price_products.grid(row=0, column=4)
        add_product_button.grid(row=0, column=5)

        self.materials = []
        for x in material.material_list:
            self.materials.append(x.name)
        if len(self.materials) == 0:
            self.materials.append('None')

        self.chosen_material = tk.StringVar(self.main_window)
        self.chosen_material.set('Select a material')
        self.material_price_entry = tk.Entry(self.main_window)
        self.material_menu = tk.OptionMenu(self.main_window, self.chosen_material, *self.materials)
        add_purchase = tk.Button(self.main_window, text='Add purchase')
        edit_entries_materials = tk.Button(self.main_window, text='Edit entries')
        add_price_materials = tk.Button(self.main_window, text='Add price point')
        add_material_button = tk.Button(self.main_window, text='Add material')

        add_material_button.bind('<Button-1>', self.add_material_click)
        add_price_materials.bind('<Button-1>', self.add_material_price_click)

        save_button = tk.Button(self.main_window, text='Save data')
        load_button = tk.Button(self.main_window, text='Load data')

        save_button.bind('<Button-1>', self.save_button_click)

        self.material_menu.grid(row=1, column=0)
        self.material_price_entry.grid(row=1, column=1)
        add_purchase.grid(row=1, column=2)
        edit_entries_materials.grid(row=1, column=3)
        add_price_materials.grid(row=1, column=4)
        add_material_button.grid(row=1, column=5)

        save_button.grid(row=2, column=5)
        load_button.grid(row=3, column=5)

        self.main_window.mainloop()

    def add_sale_click(self, event):
        self.match_product().sales += 1
        print('Sale added successfully')

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

