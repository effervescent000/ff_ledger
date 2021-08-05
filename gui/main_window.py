import tkinter as tk
from tkinter import ttk

import gui.new_material_window as nmw
import gui.new_product_window as npw
import gui.crafting_mats_window as cmw
import material
import product


class MainWindow:
    def __init__(self, xp):
        self.xp = xp
        self.main_window = tk.Tk()

        self.products = [x.name for x in product.product_list]
        self.products.sort()
        if len(self.products) == 0:
            self.products.append('None')

        # TODO figure out how to get the optionmenus to update without having to restart the application

        self.chosen_product = tk.StringVar(self.main_window)
        self.chosen_product.set('Select a product')
        self.product_price_entry = tk.Entry(self.main_window)
        self.product_combo = ttk.Combobox(self.main_window, textvariable=self.chosen_product, values=self.products)
        self.product_hq_checkbox_var = tk.IntVar(self.main_window)
        self.product_hq_checkbox = tk.Checkbutton(self.main_window, text='HQ', variable=self.product_hq_checkbox_var)
        add_sale_button = tk.Button(self.main_window, text='Add sale')
        edit_entries_products = tk.Button(self.main_window, text='Edit entries')
        add_price_products = tk.Button(self.main_window, text='Add price point')
        add_product_button = tk.Button(self.main_window, text='Add product')
        add_crafting_mats_product_button = tk.Button(self.main_window, text='Add crafting mats')

        self.product_price_var = tk.StringVar(self.main_window)
        product_stats_label = tk.Label(self.main_window, textvariable=self.product_price_var)

        add_price_products.bind('<Button-1>', self.add_product_price_click)
        add_sale_button.bind('<Button-1>', self.add_sale_click)
        add_product_button.bind('<Button-1>', self.add_product_click)
        add_crafting_mats_product_button.bind('<Button-1>', self.crafting_mats_product_click)

        product_widgets = [self.product_combo, self.product_hq_checkbox, self.product_price_entry, add_sale_button,
                           edit_entries_products, add_price_products, add_product_button,
                           add_crafting_mats_product_button]
        col = 0
        for x in product_widgets:
            x.grid(row=0, column=col)
            col += 1

        product_stats_label.grid(row=1, column=0)

        self.materials = [x.name for x in material.material_list]
        self.materials.sort()
        if len(self.materials) == 0:
            self.materials.append('None')

        self.chosen_material = tk.StringVar(self.main_window)
        self.chosen_material.set('Select a material')
        self.material_price_entry = tk.Entry(self.main_window)
        self.material_combo = ttk.Combobox(self.main_window, textvariable=self.chosen_material, values=self.materials)
        self.material_hq_checkbox_var = tk.IntVar(self.main_window)
        self.material_hq_checkbox = tk.Checkbutton(self.main_window, text='HQ', variable=self.material_hq_checkbox_var)
        add_purchase = tk.Button(self.main_window, text='Add purchase')
        edit_entries_materials = tk.Button(self.main_window, text='Edit entries')
        add_price_materials = tk.Button(self.main_window, text='Add price point')
        add_material_button = tk.Button(self.main_window, text='Add material')
        add_crafting_mats_material_button = tk.Button(self.main_window, text='Add crafting mats')

        self.material_price_var = tk.StringVar(self.main_window)
        material_stats_label = tk.Label(self.main_window, textvariable=self.material_price_var)

        add_material_button.bind('<Button-1>', self.add_material_click)
        add_price_materials.bind('<Button-1>', self.add_material_price_click)
        add_crafting_mats_material_button.bind('<Button-1>', self.crafting_mats_material_click)

        save_button = tk.Button(self.main_window, text='Save data')
        load_button = tk.Button(self.main_window, text='Load data')

        save_button.bind('<Button-1>', self.save_button_click)

        material_widgets = [self.material_combo, self.material_hq_checkbox, self.material_price_entry, add_purchase,
                            edit_entries_materials, add_price_materials, add_material_button,
                            add_crafting_mats_material_button]
        col = 0
        for x in material_widgets:
            x.grid(row=2, column=col)
            col += 1

        material_stats_label.grid(row=3, column=0)

        save_button.grid(row=4, column=5)
        load_button.grid(row=5, column=5)

        self.main_window.mainloop()

    def crafting_mats_product_click(self, event):
        cmw.CraftingMatsWindow(product.check_in_products(self.chosen_product.get()))

    def crafting_mats_material_click(self, event):
        cmw.CraftingMatsWindow(material.check_in_materials(self.chosen_material.get()))

    def display_price_product(self, name):
        try:
            self.product_price_var.set(product.check_in_products(name).get_price())
        except AttributeError:
            self.product_price_var.set('0')

    def display_price_material(self, name):
        try:
            self.material_price_var.set(material.check_in_materials(name).get_price())
        except AttributeError:
            self.material_price_var.set('0')

    def add_sale_click(self, event):
        if self.product_price_entry.get() is None:
            print('Please enter a sale value!')
        else:
            prod = self.match_product()
            prod.sales += 1
            prod.add_price_point(self.product_price_entry.get())
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
