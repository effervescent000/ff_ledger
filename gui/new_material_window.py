import tkinter as tk

import item


class NewMaterialWindow:
    def __init__(self):
        self.new_material_window = tk.Tk()

        self.material_name = tk.Entry(self.new_material_window)
        self.material_hq_var = tk.IntVar(self.new_material_window)
        self.material_hq_checkbox = tk.Checkbutton(self.new_material_window, text='HQ', variable=self.material_hq_var)
        self.material_price = tk.Entry(self.new_material_window)
        self.craftable_var = tk.IntVar(self.new_material_window)
        self.craftable_checkbox = tk.Checkbutton(self.new_material_window, text='Craftable',
                                                 variable=self.craftable_var)

        ok_button = tk.Button(self.new_material_window, text='Ok')
        cancel_button = tk.Button(self.new_material_window, text='Cancel', command=self.new_material_window.destroy)

        material_widgets = [self.material_name, self.material_hq_checkbox, self.material_price]
        col = 0
        for x in material_widgets:
            x.grid(row=0, column=col)
            col += 1

        self.craftable_checkbox.grid(row=1, column=0)

        ok_button.grid(row=1, column=2)
        cancel_button.grid(row=2, column=2)

        ok_button.bind('<ButtonRelease-1>', self.save_new_material)

    def save_new_material(self, event):
        material_result = item.check_in_materials(self.material_name)
        if material_result is not False and material_result is not None:
            material_result.add_price_point(self.material_price.get())
            print('Attempted to add an existing material to the list, updating price')
        else:
            new_material = item.Item(self.material_name.get())
            new_material.type = 'material'
            if self.material_price.get() != '':
                new_material.add_price_point(self.material_price.get())
            if self.craftable_var.get() == 0:
                new_material.craftable = False
            else:
                new_material.craftable = True
            item.material_list.append(new_material)
        self.new_material_window.destroy()
