import tkinter as tk
from tkinter import ttk

class PizzaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizza Ordering App")
        self.geometry("500x500")
        self.configure(bg="#f5e6ca")  
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for F in (OrderPage, SummaryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("OrderPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def log_order(self, order_details):
        summary_frame = self.frames["SummaryPage"]
        summary_frame.display_summary(order_details)
        self.show_frame("SummaryPage")

    def reset_order_page(self):
        order_page = self.frames["OrderPage"]
        order_page.reset_order()


class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f5e6ca")
        
        title_label = tk.Label(self, text="Welcome to Pizza Hub!", font=("Helvetica", 20), bg="#f5e6ca")
        title_label.pack(pady=10)

        self.size_label = tk.Label(self, text="Select Pizza Size:", font=("Helvetica", 14), bg="#f5e6ca")
        self.size_label.pack(pady=5)

        self.size_var = tk.StringVar(value="Medium")
        self.size_dropdown = ttk.Combobox(self, textvariable=self.size_var, values=["Small", "Medium", "Large"], state="readonly")
        self.size_dropdown.pack(pady=5)

        self.crust_label = tk.Label(self, text="Select Crust Type:", font=("Helvetica", 14), bg="#f5e6ca")
        self.crust_label.pack(pady=5)

        self.crust_var = tk.StringVar(value="Thin")
        self.crust_dropdown = ttk.Combobox(self, textvariable=self.crust_var, values=["Thin", "Thick", "Stuffed"], state="readonly")
        self.crust_dropdown.pack(pady=5)

        self.toppings_label = tk.Label(self, text="Select Toppings:", font=("Helvetica", 14), bg="#f5e6ca")
        self.toppings_label.pack(pady=5)

        self.toppings_listbox = tk.Listbox(self, selectmode="multiple", height=6)
        toppings = ["Cheese", "Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon", "Green Peppers", "Olives"]
        for topping in toppings:
            self.toppings_listbox.insert(tk.END, topping)
        self.toppings_listbox.pack(pady=5)

        self.confirm_button = ttk.Button(self, text="Confirm Order", command=self.confirm_order)
        self.confirm_button.pack(pady=20)

    def confirm_order(self):
        size = self.size_var.get()
        crust = self.crust_var.get()
        selected_toppings = [self.toppings_listbox.get(i) for i in self.toppings_listbox.curselection()]

        size_prices = {"Small": 8, "Medium": 10, "Large": 12}
        crust_prices = {"Thin": 0, "Thick": 2, "Stuffed": 3}
        topping_price = 1.5 * len(selected_toppings)

        total_price = size_prices.get(size, 0) + crust_prices.get(crust, 0) + topping_price

        order_details = {
            "size": size,
            "crust": crust,
            "toppings": selected_toppings,
            "total_price": total_price
        }

        self.controller.log_order(order_details)

    def reset_order(self):
        self.size_var.set("Medium")
        self.crust_var.set("Thin")
        self.toppings_listbox.selection_clear(0, tk.END)


class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f5e6ca")
        
        summary_title = tk.Label(self, text="Order Summary", font=("Helvetica", 20), bg="#f5e6ca")
        summary_title.pack(pady=10)
        
        self.summary_label = tk.Label(self, text="", font=("Helvetica", 14), bg="#f5e6ca", justify="left")
        self.summary_label.pack(pady=10)
        
        self.place_order_button = ttk.Button(self, text="Place Order", command=self.place_order)
        self.place_order_button.pack(pady=10)
        
        self.back_button = ttk.Button(self, text="Back to Order", command=lambda: controller.show_frame("OrderPage"))
        self.back_button.pack(pady=10)
        
    def display_summary(self, order_details):
        self.order_details = order_details
        summary_text = (
            f"Size: {order_details['size']}\n"
            f"Crust: {order_details['crust']}\n"
            f"Toppings: {', '.join(order_details['toppings']) if order_details['toppings'] else 'None'}\n"
            f"Total Price: ${order_details['total_price']:.2f}"
        )
        self.summary_label.config(text=summary_text)

    def place_order(self):
        print("Order Placed:")
        print(f"Size: {self.order_details['size']}")
        print(f"Crust: {self.order_details['crust']}")
        print(f"Toppings: {', '.join(self.order_details['toppings']) if self.order_details['toppings'] else 'None'}")
        print(f"Total Price: ${self.order_details['total_price']:.2f}")
        
        self.controller.reset_order_page()
        self.controller.show_frame("OrderPage")

if __name__ == "__main__":
    app = PizzaApp()
    app.mainloop()