import tkinter as tk
import material


class NewMaterialWindow:
    def __init__(self):
        self.new_material_window = tk.Tk()

        self.material_name = tk.Entry(self.new_material_window)
        self.material_price = tk.Entry(self.new_material_window)

        ok_button = tk.Button(self.new_material_window, text='Ok')
        cancel_button = tk.Button(self.new_material_window, text='Cancel', command=self.new_material_window.destroy)

        self.material_name.pack()
        self.material_price.pack()
        ok_button.pack()
        cancel_button.pack()

        ok_button.bind('<Button-1>', self.save_new_material)

    def save_new_material(self, event):
        material_result = material.check_in_materials(self.material_name)
        if material_result is not False and material_result is not None:
            material_result.add_price_point(self.material_price.get())
            print('Attempted to add an existing material to the list, updating price')
        else:
            new_material = material.Material(self.material_name.get())
            new_material.add_price_point(self.material_price.get())
            material.material_list.append(new_material)
