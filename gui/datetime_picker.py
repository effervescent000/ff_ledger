import datetime
import tkinter as tk
import tkcalendar as tkc


class DateTimePicker:
    def __init__(self, item, index, item_type):
        self.dt_window = tk.Tk()
        self.item = item
        self.index = index
        self.item_type = item_type

        # construct basic frames
        calendar_frame = tk.Frame(self.dt_window)
        time_frame = tk.Frame(self.dt_window)
        data_frame = tk.Frame(self.dt_window)

        # construct calendar
        self.calendar = tkc.Calendar(calendar_frame, maxdate=datetime.datetime.today())

        # construct time spinboxes
        hour_var = tk.StringVar(time_frame)
        self.hours_spin = tk.Spinbox(time_frame, from_=0, to=12, textvariable=hour_var, width=5)
        minute_var = tk.StringVar(time_frame)
        self.minutes_spin = tk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=5)
        am_pm_var = tk.StringVar(time_frame)
        self.am_pm_spin = tk.Spinbox(time_frame, values=('AM', 'PM'), width=5)

        # construct contents of data_frame
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.dt_window.destroy)

        # place frames
        calendar_frame.grid(row=0, column=0)
        time_frame.grid(row=1, column=0)
        data_frame.grid(row=2, column=0)

        # place items within frames
        self.calendar.pack()

        self.hours_spin.grid(row=0, column=0)
        self.minutes_spin.grid(row=0, column=1)
        self.am_pm_spin.grid(row=0, column=2)

        ok_button.grid(row=0, column=0)
        cancel_button.grid(row=1, column=0)
