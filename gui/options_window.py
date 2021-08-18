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

        # create contents of data_frame
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.options_window.destroy)

        ok_button.bind('<ButtonRelease-1>', self.ok_button_click)

        # place frames
        options_frame.grid(row=0, column=0)
        data_frame.grid(row=1, column=0)

        # place contents within options_frame
        self.crafting_queue_entry.grid(row=0, column=0)
        crafting_queue_label.grid(row=0, column=1)

        # place contents within data_frame
        ok_button.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0)

    def ok_button_click(self, event):
        if self.crafting_queue_entry.get() is not None:
            options.crafting_queue_length = int(self.crafting_queue_entry.get())
        self.options_window.destroy()
