import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import crafting_calc
import gui.crafting_mats_window as cmw
import gui.edit_window as ew
import gui.new_material_window as nmw
import gui.new_product_window as npw
import gui.options_window as ow
import item
import options
import price_management
from utils import get_stock


class MainWindow:
    def __init__(self, xp):
        self.xp = xp
        self.main_window = tk.Tk()
        self.cc = crafting_calc.CraftingCalc()

        # TODO implement a way to export crafting tree w/o sales/stocking data

        self.products = [x.name for x in item.product_list]
        self.products.sort()
        if len(self.products) == 0:
            self.products.append('None')

        # create upper frame and contents
        # TODO add a 'remove product' button
        self.upper_frame = tk.Frame(self.main_window)

        # TODO figure out how to get the comboboxes to update without having to restart the application
        self.chosen_product = tk.StringVar(self.upper_frame)
        self.chosen_product.set('Select a product')
        self.product_price_entry = tk.Entry(self.upper_frame)
        self.product_combo = self.AutocompleteCombobox(self.upper_frame, textvariable=self.chosen_product,
                                                       values=self.products)
        self.product_combo.set_completion_list(self.products)
        self.product_hq_checkbox_var = tk.IntVar(self.upper_frame)
        self.product_hq_checkbox = tk.Checkbutton(self.upper_frame, text='HQ', variable=self.product_hq_checkbox_var)
        add_sale_button = tk.Button(self.upper_frame, text='Add sale')
        add_stock_button = tk.Button(self.upper_frame, text='Add stock')
        edit_product = tk.Button(self.upper_frame, text='Edit')
        add_price_products = tk.Button(self.upper_frame, text='Add price point')
        add_product_button = tk.Button(self.upper_frame, text='Add product')
        add_crafting_mats_product_button = tk.Button(self.upper_frame, text='Add crafting mats')

        # create product stats
        self.product_price_var = tk.StringVar(self.upper_frame)
        product_price_label = tk.Label(self.upper_frame, textvariable=self.product_price_var)
        self.product_crafting_var = tk.StringVar(self.upper_frame)
        product_crafting_label = tk.Label(self.upper_frame, textvariable=self.product_crafting_var)
        self.product_stock_var = tk.StringVar()
        product_stock_label = tk.Label(self.upper_frame, textvariable=self.product_stock_var)

        # bind product buttons
        add_price_products.bind('<ButtonRelease-1>', self.add_product_price_click)
        edit_product.bind('<ButtonRelease-1>', self.edit_product_click)
        add_sale_button.bind('<ButtonRelease-1>', self.add_sale_click)
        add_stock_button.bind('<ButtonRelease-1>', self.add_stock_click)
        add_product_button.bind('<ButtonRelease-1>', self.add_product_click)
        add_crafting_mats_product_button.bind('<ButtonRelease-1>', self.crafting_mats_product_click)
        self.product_combo.bind('<<ComboboxSelected>>', self.display_stats_product)

        # place product widgets
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

        # create material contents
        # TODO add a 'remove material' button
        self.materials = [x.name for x in item.material_list]
        self.materials.sort()
        if len(self.materials) == 0:
            self.materials.append('None')

        self.chosen_material = tk.StringVar(self.upper_frame)
        self.chosen_material.set('Select a material')
        self.material_price_entry = tk.Entry(self.upper_frame)
        self.material_combo = self.AutocompleteCombobox(self.upper_frame, textvariable=self.chosen_material,
                                                        values=self.materials)
        self.material_combo.set_completion_list(self.materials)
        self.material_hq_checkbox_var = tk.IntVar(self.upper_frame)
        self.material_hq_checkbox = tk.Checkbutton(self.upper_frame, text='HQ', variable=self.material_hq_checkbox_var)
        add_purchase = tk.Button(self.upper_frame, text='Add purchase')
        edit_material = tk.Button(self.upper_frame, text='Edit')
        add_price_materials = tk.Button(self.upper_frame, text='Add price point')
        add_material_button = tk.Button(self.upper_frame, text='Add material')
        add_crafting_mats_material_button = tk.Button(self.upper_frame, text='Add crafting mats')

        # create material stats
        self.material_price_var = tk.StringVar()
        material_price_label = tk.Label(self.upper_frame, textvariable=self.material_price_var)
        self.material_crafting_var = tk.StringVar()
        material_crafting_label = tk.Label(self.upper_frame, textvariable=self.material_crafting_var)

        # bind material buttons
        add_material_button.bind('<ButtonRelease-1>', self.add_material_click)
        edit_material.bind('<ButtonRelease-1>', self.edit_material_click)
        add_price_materials.bind('<ButtonRelease-1>', self.add_material_price_click)
        add_crafting_mats_material_button.bind('<ButtonRelease-1>', self.crafting_mats_material_click)
        self.material_combo.bind('<<ComboboxSelected>>', self.display_stats_material)

        # place material widgets
        material_widgets = [self.material_combo, self.material_hq_checkbox, self.material_price_entry, add_purchase,
                            edit_material, add_price_materials, add_material_button,
                            add_crafting_mats_material_button]
        col = 0
        for x in material_widgets:
            x.grid(row=2, column=col)
            col += 1

        material_price_label.grid(row=3, column=0)
        material_crafting_label.grid(row=3, column=2)

        # create data frame and contents
        data_frame = tk.Frame(self.main_window)
        save_button = tk.Button(data_frame, text='Save data')
        load_button = tk.Button(data_frame, text='Load data')
        # TODO make the load button do something lol
        craft_queue_button = tk.Button(data_frame, text='Crafting queue')
        purge_data_button = tk.Button(data_frame, text='Purge records')
        options_button = tk.Button(data_frame, text='Options')
        # TODO add a 'price check' (or something) button that will print items w/o recent price data to warning text
        purge_prices_button = tk.Button(data_frame, text='Purge old price data')

        save_button.bind('<ButtonRelease-1>', self.save_button_click)
        craft_queue_button.bind('<ButtonRelease-1>', self.craft_queue_button_click)
        purge_data_button.bind('<ButtonRelease-1>', self.purge_records_button_click)
        options_button.bind('<ButtonRelease-1>', self.options_button_click)
        purge_prices_button.bind('<ButtonRelease-1>', self.purge_prices_button_click)

        data_widgets = [save_button, load_button, craft_queue_button, purge_data_button, purge_prices_button,
                        options_button]
        i = 0
        for x in data_widgets:
            x.grid(row=i, column=0)
            i += 1

        # stock display
        self.stock_frame = tk.Frame(self.main_window)
        stock_label = tk.Label(self.stock_frame, text='Current stock')
        stock_label.grid(row=0, column=0, columnspan=2)
        self.stock_list = get_stock()
        for i in range(1, len(self.stock_list)):
            for j in range(len(self.stock_list[0])):
                e = tk.Entry(self.stock_frame)
                e.grid(row=i, column=j)
                e.insert(0, self.stock_list[i][j])

        # output frame and contents
        output_frame = tk.Frame(self.main_window)
        # craft_queue_var = tk.StringVar(output_frame)
        self.crafting_queue_text = tk.Text(output_frame, width=50, height=15)
        self.warnings_text = tk.Text(output_frame, width=50, height=15)

        self.crafting_queue_text.grid(row=0, column=0)
        self.warnings_text.grid(row=1, column=0)

        # place frames
        self.upper_frame.grid(row=0, column=0, columnspan=3)
        self.stock_frame.grid(row=1, column=0)
        data_frame.grid(row=1, column=1, padx=2)
        output_frame.grid(row=1, column=2)

        self.main_window.mainloop()

    def edit_product_click(self, event):
        ew.EditWindow(item.check_in_products(self.product_combo.get()))

    def edit_material_click(self, event):
        ew.EditWindow(item.check_in_materials(self.material_combo.get()))

    def purge_records_button_click(self, event):
        answer = messagebox.askyesno('Confirmation', 'Are you SURE you want to purge your data?')
        if answer is True:
            self.xp.backup_data()
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

    def purge_prices_button_click(self, event):
        price_management.purge_old_price_data(self.warnings_text)

    def craft_queue_button_click(self, event):
        craft_queue = self.cc.get_crafts(options.crafting_queue_length, self.warnings_text)
        # clear the crafting queue text before writing to it
        self.crafting_queue_text.delete(1.0, tk.END)
        for x in craft_queue:
            output_string = '{} for {} {}\n'.format(x.name, x.profit, x.units)
            self.crafting_queue_text.insert(tk.END, output_string)

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
            self.product_crafting_var.set(self.cc.get_crafting_cost(prod, self.warnings_text))
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
            self.material_crafting_var.set(self.cc.get_crafting_cost(mat, self.warnings_text))

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

    def options_button_click(self, event):
        ow.OptionsWindow()

    class AutocompleteCombobox(ttk.Combobox):
        """Code taken from https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html"""

        # TODO move this class to its own file and use it in the crafting mats window
        def set_completion_list(self, completion_list):
            """Use our completion list as our drop down selection menu, arrows move through menu."""
            self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
            self._hits = []
            self._hit_index = 0
            self.position = 0
            self.bind('<KeyRelease>', self.handle_keyrelease)
            self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
            """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
            if delta:  # need to delete selection otherwise we would fix the current position
                self.delete(self.position, tk.END)
            else:  # set position to end so selection starts where textentry ended
                self.position = len(self.get())
            # collect hits
            _hits = []
            for element in self._completion_list:
                if element.lower().startswith(self.get().lower()):  # Match case insensitively
                    _hits.append(element)
            # if we have a new hit list, keep this in mind
            if _hits != self._hits:
                self._hit_index = 0
                self._hits = _hits
            # only allow cycling if we are in a known hit list
            if _hits == self._hits and self._hits:
                self._hit_index = (self._hit_index + delta) % len(self._hits)
            # now finally perform the auto completion
            if self._hits:
                self.delete(0, tk.END)
                self.insert(0, self._hits[self._hit_index])
                self.select_range(self.position, tk.END)

        def handle_keyrelease(self, event):
            """event handler for the keyrelease event on this widget"""
            if event.keysym == "BackSpace":
                self.delete(self.index(tk.INSERT), tk.END)
                self.position = self.index(tk.END)
            if event.keysym == "Left":
                if self.position < self.index(tk.END):  # delete the selection
                    self.delete(self.position, tk.END)
                else:
                    self.position = self.position - 1  # delete one character
                    self.delete(self.position, tk.END)
            if event.keysym == "Right":
                self.position = self.index(tk.END)  # go to end (no selection)
            if len(event.keysym) == 1:
                self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion
