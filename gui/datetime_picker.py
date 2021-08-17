import datetime
import tkinter as tk
import tkcalendar as tkc
import xml_parser as xp


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
        self.calendar = tkc.Calendar(
            calendar_frame,
            maxdate=datetime.datetime.today(),
            date_pattern='y-mm-dd'
        )

        # construct time spinboxes
        hour_var = tk.StringVar(time_frame)
        self.hours_spin = tk.Spinbox(
            time_frame,
            from_=0,
            to=12,
            textvariable=hour_var,
            width=5)
        minute_var = tk.StringVar(time_frame)
        self.minutes_spin = tk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=5)
        am_pm_var = tk.StringVar(time_frame)
        self.am_pm_spin = tk.Spinbox(time_frame, values=('AM', 'PM'), width=5)

        # construct contents of data_frame
        ok_button = tk.Button(data_frame, text='Ok')
        cancel_button = tk.Button(data_frame, text='Cancel', command=self.dt_window.destroy)

        ok_button.bind('<ButtonRelease-1>', self.ok_button_click)

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

    def ok_button_click(self, event):
        # construct a datetime from the relevant elements
        date_string = self.calendar.get_date()
        # convert AM/PM time to 24 hr time b/c im too dumb to do it in my head
        time_hours = int(self.hours_spin.get())
        time_am_pm = self.am_pm_spin.get()
        if time_hours == 12:
            time_hours = 0
        if time_am_pm == 'PM':
            time_hours += 12
        time_string = '{}:{}'.format(
            str(time_hours),
            self.minutes_spin.get())
        new_datetime = datetime.datetime.strptime('{} {}'.format(date_string, time_string), xp.time_format)
        if self.item_type == 'sales':
            self.item.sales_data[self.index] = new_datetime
        elif self.item_type == 'stock':
            self.item.stock_data[self.index] = new_datetime
        else:
            print('Invalid item_type passed to datetime_picker!')
        self.dt_window.destroy()
