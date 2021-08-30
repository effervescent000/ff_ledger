import tkinter as tk
import options


class OptionsWindow:
    def __init__(self):
        self.options_window = tk.Tk()

        # create frames
        options_frame = tk.Frame(self.options_window)
        data_frame = tk.Frame(self.options_window)

        # create contents of options_frame
        crafting_queue_var = tk.StringVar(options_frame)
        crafting_queue_var.set(str(options.crafting_queue_length))
        self.crafting_queue_entry = tk.Entry(options_frame, textvariable=crafting_queue_var, width=5)
        crafting_queue_label = tk.Label(options_frame, text='Length of crafting queue')

        time_gap_var = tk.StringVar(options_frame)
        time_gap_var.set(str(options.time_gap))
        self.time_gap_entry = tk.Entry(options_frame, textvariable=time_gap_var, width=5)
        time_gap_label = tk.Label(options_frame, text='Maximum time gap for match_stock')

        # TODO add options related to price purging

        # create contents of data_frame
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.options_window.destroy)
        # TODO add a 'reset options to defaults' button

        ok_button.bind('<ButtonRelease-1>', self.ok_button_click)

        # place frames
        options_frame.grid(row=0, column=0)
        data_frame.grid(row=1, column=0)

        # place contents within options_frame
        entry_list = [self.crafting_queue_entry, self.time_gap_entry]
        label_list = [crafting_queue_label, time_gap_label]
        row = 0
        for x in entry_list:
            x.grid(row=row, column=0)
            row += 1
        row = 0
        for x in label_list:
            x.grid(row=row, column=1)
            row += 1
        self.crafting_queue_entry.grid(row=0, column=0)
        crafting_queue_label.grid(row=0, column=1)

        # place contents within data_frame
        ok_button.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0)

    def ok_button_click(self, event):
        if self.crafting_queue_entry.get() is not None:
            options.crafting_queue_length = int(self.crafting_queue_entry.get())
        self.options_window.destroy()
