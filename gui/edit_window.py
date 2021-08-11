import tkinter as tk


class EditWindow:
    def __init__(self, item):
        # TODO add a way to edit sales/stocks amounts directly and/or a way to edit sales/stocking entries
        self.item = item
        self.edit_window = tk.Tk()
        edit_frame = tk.Frame(self.edit_window)
        self.item_name = tk.Entry(edit_frame)
        self.item_name.insert(0, self.item.name)
        self.craftable_var = tk.IntVar(edit_frame)
        if self.item.craftable is True:
            self.craftable_var.set(1)
        craftable_checkbox = tk.Checkbutton(edit_frame, text='Craftable', variable=self.craftable_var)

        data_frame = tk.Frame(self.edit_window)
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.edit_window.destroy)

        edit_frame.grid(row=0, column=0)
        data_frame.grid(row=1, column=0)

        self.item_name.grid(row=0, column=0)
        craftable_checkbox.grid(row=0, column=1)

        ok_button.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0)

        ok_button.bind('<Button-1>', self.save_button_click)

    def save_button_click(self, event):
        self.item.name = self.item_name.get()
        if self.craftable_var.get() == 0:
            self.item.craftable = False
        else:
            self.item.craftable = True
        self.edit_window.destroy()
