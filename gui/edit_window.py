import tkinter as tk
import gui.datetime_picker as dtp
import utils
import datetime


class EditWindow:
    def __init__(self, item):
        # TODO add labels to frames
        self.item = item
        self.edit_window = tk.Tk()

        # edit frame and contents
        edit_frame = tk.Frame(self.edit_window)
        self.item_name = tk.Entry(edit_frame)
        self.item_name.insert(0, self.item.name)
        self.craftable_var = tk.IntVar(edit_frame)
        if self.item.craftable is True:
            self.craftable_var.set(1)
        craftable_checkbox = tk.Checkbutton(edit_frame, text='Craftable', variable=self.craftable_var)

        # stock list frame and contents
        stock_frame = tk.Frame(self.edit_window)
        self.stock_item_list = []

        if len(self.item.stock_data) > 0:
            for x in reversed(self.item.stock_data):
                time_var = tk.StringVar(stock_frame)
                time_var.set(x.strftime(utils.time_format))
                time_entry = tk.Entry(stock_frame, textvariable=time_var, state=tk.DISABLED)
                time_entry.bind('<ButtonRelease-1>', self.edit_time_click)
                self.stock_item_list.append(time_entry)

        # sales list frame and contents
        sales_frame = tk.Frame(self.edit_window)
        self.sales_item_list = []

        if len(self.item.sales_data) > 0:
            # TODO update this to also include a price from a matching time to be editable, for now just doing the times
            for x in reversed(self.item.sales_data):
                time_var = tk.StringVar(sales_frame)
                time_var.set(x.strftime(utils.time_format))
                time_entry = tk.Entry(sales_frame, textvariable=time_var, state=tk.DISABLED)
                time_entry.bind('<ButtonRelease-1>', self.edit_time_click)
                self.sales_item_list.append(time_entry)

        # data frame and contents
        data_frame = tk.Frame(self.edit_window)
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.edit_window.destroy)

        ok_button.bind('<Button-1>', self.save_button_click)

        # place frames
        edit_frame.grid(row=0, column=0, columnspan=2)
        stock_frame.grid(row=1, column=0)
        sales_frame.grid(row=1, column=1)
        data_frame.grid(row=1, column=2)

        # place items within frames
        self.item_name.grid(row=0, column=0)
        craftable_checkbox.grid(row=0, column=1)

        # stock frame
        i = 0
        for x in self.stock_item_list:
            x.grid(row=i, column=0)
            i += 1

        # sales frame
        i = 0
        for x in self.sales_item_list:
            x.grid(row=i, column=0)
            i += 1

        ok_button.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0)

    def save_button_click(self, event):
        self.item.name = self.item_name.get()
        if self.craftable_var.get() == 0:
            self.item.craftable = False
        else:
            self.item.craftable = True
        self.edit_window.destroy()

    def edit_time_click(self, event):
        time_item = event.widget.get()
        print(time_item)
        item_type = None
        if event.widget in self.sales_item_list:
            item_type = 'sales'
        elif event.widget in self.stock_item_list:
            item_type = 'stock'
        else:
            print('Event.widget is somehow not in either sales_item_list or stock_item_list')
        time_item = datetime.datetime.strptime(time_item, utils.time_format)
        if time_item in self.item.stock_data:
            time_index = self.item.stock_data.index(time_item)
            dtp.DateTimePicker(self.item, time_index, item_type)
        elif time_item in self.item.sales_data:
            time_index = self.item.sales_data.index(time_item)
            dtp.DateTimePicker(self.item, time_index, item_type)
        else:
            print('Somehow time_item {} is not in stock_data or sales_data for {}'.format(str(time_item), self.item.name))
