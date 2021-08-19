import tkinter as tk
from tkinter import ttk

import item


class CraftingMatsWindow:
    def __init__(self, root_item):
        self.root_item = root_item
        self.crafting_mats_window = tk.Tk()

        self.quantity_1_entry = tk.Entry(self.crafting_mats_window)
        self.quantity_2_entry = tk.Entry(self.crafting_mats_window)
        self.quantity_3_entry = tk.Entry(self.crafting_mats_window)
        self.quantity_4_entry = tk.Entry(self.crafting_mats_window)
        self.quantity_5_entry = tk.Entry(self.crafting_mats_window)

        quantity_widgets = [self.quantity_1_entry, self.quantity_2_entry, self.quantity_3_entry, self.quantity_4_entry,
                            self.quantity_5_entry]
        r = 0
        for x in quantity_widgets:
            x.grid(row=r, column=0)
            r += 1

        option_list = [x.name for x in item.material_list]
        option_list.sort()

        self.item_1_var = tk.StringVar(self.crafting_mats_window)
        self.item_2_var = tk.StringVar(self.crafting_mats_window)
        self.item_3_var = tk.StringVar(self.crafting_mats_window)
        self.item_4_var = tk.StringVar(self.crafting_mats_window)
        self.item_5_var = tk.StringVar(self.crafting_mats_window)

        self.item_1_combo = ttk.Combobox(self.crafting_mats_window, textvariable=self.item_1_var, values=option_list)
        self.item_2_combo = ttk.Combobox(self.crafting_mats_window, textvariable=self.item_2_var, values=option_list)
        self.item_3_combo = ttk.Combobox(self.crafting_mats_window, textvariable=self.item_3_var, values=option_list)
        self.item_4_combo = ttk.Combobox(self.crafting_mats_window, textvariable=self.item_4_var, values=option_list)
        self.item_5_combo = ttk.Combobox(self.crafting_mats_window, textvariable=self.item_5_var, values=option_list)

        item_widgets = [self.item_1_combo, self.item_2_combo, self.item_3_combo, self.item_4_combo, self.item_5_combo]
        r = 0
        for x in item_widgets:
            x.grid(row=r, column=1)
            r += 1

        self.ok_button = tk.Button(self.crafting_mats_window, text='Ok')
        self.cancel_button = tk.Button(self.crafting_mats_window, text='Cancel',
                                       command=self.crafting_mats_window.destroy)

        self.ok_button.grid(row=5, column=1)
        self.cancel_button.grid(row=6, column=1)

        self.ok_button.bind('<ButtonRelease-1>', self.save_button_click)

        # populate crafting reagents if this item already has them assigned
        if len(self.root_item.reagents) > 0:
            i = 0
            for x in self.root_item.reagents.items():
                quantity_widgets[i].insert(0, str(x[1]))
                item_widgets[i].insert(0, x[0])
                i += 1

    def save_button_click(self, event):
        # first, if the item already has crafting reagents set, purge them to avoid duplicates
        if len(self.root_item.reagents) > 0:
            self.root_item.reagents = {}

        # now set reagents as normal
        if self.item_1_var.get() is not '':
            self.add_crafting_reagent(1)
        if self.item_2_var.get() is not '':
            self.add_crafting_reagent(2)
        if self.item_3_var.get() is not '':
            self.add_crafting_reagent(3)
        if self.item_4_var.get() is not '':
            self.add_crafting_reagent(4)
        if self.item_5_var.get() is not '':
            self.add_crafting_reagent(5)
        self.crafting_mats_window.destroy()

    def add_crafting_reagent(self, num):
        if num == 1:
            k = item.check_in_materials(self.item_1_var.get())
            v = self.quantity_1_entry.get()
        elif num == 2:
            k = item.check_in_materials(self.item_2_var.get())
            v = self.quantity_2_entry.get()
        elif num == 3:
            k = item.check_in_materials(self.item_3_var.get())
            v = self.quantity_3_entry.get()
        elif num == 4:
            k = item.check_in_materials(self.item_4_var.get())
            v = self.quantity_4_entry.get()
        elif num == 5:
            k = item.check_in_materials(self.item_5_var.get())
            v = self.quantity_5_entry.get()
        if v is None:
            v = 1
        self.root_item.reagents[k.name] = v
