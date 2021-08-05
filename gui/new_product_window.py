import tkinter as tk
import product


class NewProductWindow:
    def __init__(self):
        self.new_product_window = tk.Tk()

        self.product_name = tk.Entry(self.new_product_window)
        self.product_price = tk.Entry(self.new_product_window)

        ok_button = tk.Button(self.new_product_window, text='Ok')
        cancel_button = tk.Button(self.new_product_window, text='Cancel', command=self.new_product_window.destroy)

        self.product_name.pack()
        self.product_price.pack()
        ok_button.pack()
        cancel_button.pack()

        ok_button.bind('<Button-1>', self.save_new_product)

    def save_new_product(self, event):
        product_result = product.check_in_products(self.product_name)
        if product_result is not False and product_result is not None:
            product_result.add_price_point(self.product_price.get())
            print('Attempted to add an existing product to the list, updating price')
        else:
            new_product = product.Product(self.product_name.get())
            new_product.add_price_point(self.product_price.get())
            product.product_list.append(new_product)
        self.new_product_window.destroy()
