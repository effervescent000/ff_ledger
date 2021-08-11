import tkinter as tk
from tkinter import ttk

import crafting_calc
import gui.crafting_mats_window as cmw
import gui.edit_window as ew
import gui.new_material_window as nmw
import gui.new_product_window as npw
import item


class MainWindow:
    def __init__(self, xp):
        # TODO add a "craftable" checkbox somewhere (not necessarily in main_window)
        self.xp = xp
        self.main_window = tk.Tk()
        self.cc = crafting_calc.CraftingCalc()

        # TODO implement a way to export crafting tree w/o sales/stocking data

        self.products = [x.name for x in item.product_list]
        self.products.sort()
        if len(self.products) == 0:
            self.products.append('None')

        # TODO figure out how to get the optionmenus to update without having to restart the application

        self.upper_frame = tk.Frame(self.main_window)

        self.chosen_product = tk.StringVar(self.upper_frame)
        self.chosen_product.set('Select a product')
        self.product_price_entry = tk.Entry(self.upper_frame)
        self.product_combo = ttk.Combobox(self.upper_frame, textvariable=self.chosen_product, values=self.products)
        self.product_hq_checkbox_var = tk.IntVar(self.upper_frame)
        self.product_hq_checkbox = tk.Checkbutton(self.upper_frame, text='HQ', variable=self.product_hq_checkbox_var)
        add_sale_button = tk.Button(self.upper_frame, text='Add sale')
        add_stock_button = tk.Button(self.upper_frame, text='Add stock')
        edit_product = tk.Button(self.upper_frame, text='Edit')
        add_price_products = tk.Button(self.upper_frame, text='Add price point')
        add_product_button = tk.Button(self.upper_frame, text='Add product')
        add_crafting_mats_product_button = tk.Button(self.upper_frame, text='Add crafting mats')

        self.product_price_var = tk.StringVar(self.upper_frame)
        product_price_label = tk.Label(self.upper_frame, textvariable=self.product_price_var)
        self.product_crafting_var = tk.StringVar(self.upper_frame)
        product_crafting_label = tk.Label(self.upper_frame, textvariable=self.product_crafting_var)
        self.product_stock_var = tk.StringVar()
        product_stock_label = tk.Label(self.upper_frame, textvariable=self.product_stock_var)

        add_price_products.bind('<Button-1>', self.add_product_price_click)
        edit_product.bind('<Button-1>', self.edit_product_click)
        add_sale_button.bind('<Button-1>', self.add_sale_click)
        add_stock_button.bind('<Button-1>', self.add_stock_click)
        add_product_button.bind('<Button-1>', self.add_product_click)
        add_crafting_mats_product_button.bind('<Button-1>', self.crafting_mats_product_click)
        self.product_combo.bind('<<ComboboxSelected>>', self.display_stats_product)

        product_widgets = [self.product_combo, self.product_hq_checkbox, self.product_price_entry, add_sale_button,
                           add_stock_button, edit_product, add_price_products, add_product_button,
                           add_crafting_mats_product_button]
        col = 0
        for x in product_widgets:
            x.grid(row=0, column=col)
            col += 1

        product_price_label.grid(row=1, column=0)
        product_crafting_label.grid(row=1, column=2)
        product_stock_label.grid(row=1, column=3)

        self.materials = [x.name for x in item.material_list]
        self.materials.sort()
        if len(self.materials) == 0:
            self.materials.append('None')

        self.chosen_material = tk.StringVar(self.upper_frame)
        self.chosen_material.set('Select a material')
        self.material_price_entry = tk.Entry(self.upper_frame)
        self.material_combo = ttk.Combobox(self.upper_frame, textvariable=self.chosen_material, values=self.materials)
        self.material_hq_checkbox_var = tk.IntVar(self.upper_frame)
        self.material_hq_checkbox = tk.Checkbutton(self.upper_frame, text='HQ', variable=self.material_hq_checkbox_var)
        add_purchase = tk.Button(self.upper_frame, text='Add purchase')
        edit_material = tk.Button(self.upper_frame, text='Edit')
        add_price_materials = tk.Button(self.upper_frame, text='Add price point')
        add_material_button = tk.Button(self.upper_frame, text='Add material')
        add_crafting_mats_material_button = tk.Button(self.upper_frame, text='Add crafting mats')

        self.material_price_var = tk.StringVar()
        material_price_label = tk.Label(self.upper_frame, textvariable=self.material_price_var)
        self.material_crafting_var = tk.StringVar()
        material_crafting_label = tk.Label(self.upper_frame, textvariable=self.material_crafting_var)

        add_material_button.bind('<Button-1>', self.add_material_click)
        edit_material.bind('<Button-1>', self.edit_material_click)
        add_price_materials.bind('<Button-1>', self.add_material_price_click)
        add_crafting_mats_material_button.bind('<Button-1>', self.crafting_mats_material_click)
        self.material_combo.bind('<<ComboboxSelected>>', self.display_stats_material)

        material_widgets = [self.material_combo, self.material_hq_checkbox, self.material_price_entry, add_purchase,
                            edit_material, add_price_materials, add_material_button,
                            add_crafting_mats_material_button]
        col = 0
        for x in material_widgets:
            x.grid(row=2, column=col)
            col += 1

        material_price_label.grid(row=3, column=0)
        material_crafting_label.grid(row=3, column=2)

        self.data_frame = tk.Frame(self.main_window)
        save_button = tk.Button(self.data_frame, text='Save data')
        load_button = tk.Button(self.data_frame, text='Load data')
        craft_queue_button = tk.Button(self.data_frame, text='Crafting queue')
        purge_button = tk.Button(self.data_frame, text='Purge data')

        save_button.bind('<Button-1>', self.save_button_click)
        craft_queue_button.bind('<Button-1>', self.craft_queue_button_click)
        purge_button.bind('<Button-1>', self.purge_button_click)

        save_button.grid(row=4, column=5)
        load_button.grid(row=5, column=5)
        craft_queue_button.grid(row=6, column=5)
        purge_button.grid(row=7, column=5)

        # now beginning stock display
        self.stock_frame = tk.Frame(self.main_window)
        self.stock_list = self.cc.get_stock()
        for i in range(len(self.stock_list)):
            for j in range(len(self.stock_list[0])):
                e = tk.Entry(self.stock_frame)
                e.grid(row=i, column=j)
                e.insert(0, self.stock_list[i][j])

        # place frames
        self.upper_frame.grid(row=0, column=0, columnspan=2)
        self.stock_frame.grid(row=1, column=0)
        self.data_frame.grid(row=1, column=1)

        self.main_window.mainloop()

    def edit_product_click(self, event):
        ew.EditWindow(item.check_in_products(self.product_combo.get()))

    def edit_material_click(self, event):
        ew.EditWindow(item.check_in_materials(self.material_combo.get()))

    def purge_button_click(self, event):
        # TODO add an automatic backup to this (or possibly to the save button, just SOMEWHERE
        for x in item.product_list:
            x.stock_data = []
            x.price_data = []
            x.sales_data = []
            x.price = 0
            x.sales = 0
            x.stock = 0
        for x in item.material_list:
            x.price_data = []
            x.price = 0
            x.stock_data = []
            x.stock = 0

    def craft_queue_button_click(self, event):
        # TODO add a way to select the number of crafts from the GUI
        craft_queue = self.cc.get_crafts(5)
        for x in craft_queue:
            print('{} for {} {}'.format(x.name, x.profit, x.units))

    def crafting_mats_product_click(self, event):
        cmw.CraftingMatsWindow(item.check_in_products(self.chosen_product.get()))

    def crafting_mats_material_click(self, event):
        cmw.CraftingMatsWindow(item.check_in_materials(self.chosen_material.get()))

    def display_stats_product(self, event=None):
        prod = item.check_in_products(self.product_combo.get())
        try:
            self.product_price_var.set(prod.get_price())
        except AttributeError:
            self.product_price_var.set('0')
        if len(prod.reagents) == 0:
            self.product_crafting_var.set('0')
        else:
            self.product_crafting_var.set(self.cc.get_crafting_cost(prod))
        self.product_stock_var.set(prod.stock)

    def display_stats_material(self, event=None):
        mat = item.check_in_materials(self.material_combo.get())
        try:
            self.material_price_var.set(mat.get_price())
        except AttributeError:
            self.material_price_var.set('0')
        if len(mat.reagents) == 0:
            self.material_crafting_var.set('0')
        else:
            self.material_crafting_var.set(self.cc.get_crafting_cost(mat))

    def add_sale_click(self, event):
        if self.product_price_entry.get() is '':
            print('Please enter a sale value!')
        else:
            prod = item.check_in_products(self.product_combo.get())
            prod.add_sale()
            prod.add_price_point(int(self.product_price_entry.get()) / .95)
            self.display_stats_product()

    def add_stock_click(self, event):
        prod = item.check_in_products(self.product_combo.get())
        prod.add_stock()
        self.display_stats_product()

    def add_product_price_click(self, event):
        if self.chosen_product is not None and self.product_price_entry.get() is not None:
            prod = item.check_in_products(self.chosen_product.get())
            if prod is not False:
                prod.add_price_point(self.product_price_entry.get())
                self.display_stats_product()

    def add_material_price_click(self, event):
        if self.chosen_material is not None and self.material_price_entry.get() is not None:
            mat = item.check_in_materials((self.chosen_material.get()))
            if mat is not False:
                mat.add_price_point(self.material_price_entry.get())
                self.display_stats_material()

    def add_material_click(self, event):
        nmw.NewMaterialWindow()

    def add_product_click(self, event):
        npw.NewProductWindow()

    def save_button_click(self, event):
        for x in item.product_list:
            x.prep_for_records()
            self.xp.add_item_to_xml(x)
        for x in item.material_list:
            x.prep_for_records()
            self.xp.add_item_to_xml(x)

        self.xp.save_xml()
        self.main_window.destroy()
