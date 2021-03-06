import tkinter as tk

import item


class NewProductWindow:
    def __init__(self):
        self.new_product_window = tk.Tk()

        self.product_name = tk.Entry(self.new_product_window)
        self.product_price = tk.Entry(self.new_product_window)

        ok_button = tk.Button(self.new_product_window, text='Ok')
        cancel_button = tk.Button(self.new_product_window, text='Cancel', command=self.new_product_window.destroy)

        product_widgets = [self.product_name, self.product_price]
        col = 0
        for x in product_widgets:
            x.grid(row=0, column=col)
            col += 1

        ok_button.grid(row=1, column=2)
        cancel_button.grid(row=2, column=2)

        ok_button.bind('<ButtonRelease-1>', self.save_new_product)

    def save_new_product(self, event):
        product_result = item.check_in_products(self.product_name)
        price = self.product_price.get()
        if product_result is not False and product_result is not None:
            if price != '':
                product_result.add_price_point(price)
                print('Attempted to add an existing product to the list, updating price')
        else:
            new_product = item.Item(self.product_name.get())
            new_product.type = 'product'
            if price != '':
                new_product.add_price_point(self.product_price.get())
            item.product_list.append(new_product)
        self.new_product_window.destroy()
