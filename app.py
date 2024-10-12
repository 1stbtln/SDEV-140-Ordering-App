import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  
import os

class PizzaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizza Ordering App")
        self.geometry("800x800")  
        self.configure(bg="#2e2e2e")  

        pizza_image_path = "bag.png"
        logo_image_path = "logo.png"
                
        self.img_pizza = self.load_image(pizza_image_path, "Pizza Image", (200, 200))  # Resize pizza image
        self.img_logo = self.load_image(logo_image_path, "Pizza Logo", (200, 200))  # Resize logo to 200x200

        container = tk.Frame(self, bg="#2e2e2e")
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (OrderPage, SummaryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("OrderPage")

    def load_image(self, img_path, alt_text, size=None):
        """Load image from the specified path and optionally resize it."""
        try:
            image = Image.open(img_path)
            if size:
                image = image.resize(size) 
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {alt_text}: {e}")
            return None

    def show_frame(self, page_name):
        """Raise a frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

    def log_order(self, order_details):
        """Pass order details to the summary page."""
        summary_frame = self.frames["SummaryPage"]
        summary_frame.display_summary(order_details)
        self.show_frame("SummaryPage")

    def reset_order_page(self):
        """Reset the order page for a new order."""
        order_page = self.frames["OrderPage"]
        order_page.reset_order()

class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2e2e2e")  

        center_frame = tk.Frame(self, bg="#2e2e2e")
        center_frame.pack(expand=True)

        title_label = tk.Label(center_frame, text="Welcome to Home Fire Pizza!", font=("Helvetica", 20), bg="#2e2e2e", fg="#f5e6ca")
        title_label.pack(pady=20)

        if controller.img_logo: 
            logo_label = tk.Label(center_frame, image=controller.img_logo, bg="#2e2e2e")
            logo_label.image = controller.img_logo 
            logo_label.pack(pady=10)

        self.size_label = tk.Label(center_frame, text="Select Pizza Size:", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca")
        self.size_label.pack(pady=5)

        self.size_var = tk.StringVar(value="Medium")
        self.size_dropdown = ttk.Combobox(center_frame, textvariable=self.size_var, values=["Small", "Medium", "Large"], state="readonly", 
                                           background="#3e3e3e", foreground="#f5e6ca")
        self.size_dropdown.pack(pady=5)

        self.toppings_label = tk.Label(center_frame, text="Select Toppings:", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca")
        self.toppings_label.pack(pady=5)

        self.toppings_listbox = tk.Listbox(center_frame, selectmode="multiple", height=6, bg="#3e3e3e", fg="#f5e6ca", selectbackground="#5e5e5e")
        toppings = ["Cheese", "Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon", "Green Peppers", "Olives"]
        for topping in toppings:
            self.toppings_listbox.insert(tk.END, topping)
        self.toppings_listbox.pack(pady=5)

        self.confirm_button = ttk.Button(center_frame, text="Confirm Order", command=self.confirm_order)
        self.confirm_button.pack(pady=20)

        self.exit_button = ttk.Button(center_frame, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def confirm_order(self):
        """Handle order confirmation and pass the data to the summary page."""
        size = self.size_var.get()
        selected_toppings = [self.toppings_listbox.get(i) for i in self.toppings_listbox.curselection()]

        if not selected_toppings:
            messagebox.showwarning("Warning", "Please select at least one topping.")
            return

        size_prices = {"Small": 8, "Medium": 10, "Large": 12}
        total_price = size_prices.get(size, 0) + (1.5 * len(selected_toppings))

        order_details = {
            "size": size,
            "toppings": selected_toppings,
            "total_price": total_price
        }

        self.controller.log_order(order_details)

    def reset_order(self):
        """Reset order form to default state."""
        self.size_var.set("Medium")
        self.toppings_listbox.selection_clear(0, tk.END)

    def exit_app(self):
        """Handle exiting the application."""
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.controller.destroy()

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2e2e2e")  

        center_frame = tk.Frame(self, bg="#2e2e2e")
        center_frame.pack(expand=True)

        if controller.img_pizza: 
            pizza_label = tk.Label(center_frame, image=controller.img_pizza, bg="#2e2e2e")
            pizza_label.image = controller.img_pizza 
            pizza_label.pack(pady=10)

        summary_title = tk.Label(center_frame, text="Order Summary", font=("Helvetica", 20), bg="#2e2e2e", fg="#f5e6ca")
        summary_title.pack(pady=20)

        self.summary_label = tk.Label(center_frame, text="", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca", justify="left")
        self.summary_label.pack(pady=10)

        self.place_order_button = ttk.Button(center_frame, text="Place Order", command=self.place_order)
        self.place_order_button.pack(pady=10)

        self.back_button = ttk.Button(center_frame, text="Back to Order", command=lambda: controller.show_frame("OrderPage"))
        self.back_button.pack(pady=5)

    def display_summary(self, order_details):
        """Display the summary of the order."""
        self.order_details = order_details
        summary_text = (
            f"Size: {order_details['size']}\n"
            f"Toppings: {', '.join(order_details['toppings'])}\n"
            f"Total Price: ${order_details['total_price']:.2f}"
        )
        self.summary_label.config(text=summary_text)

    def place_order(self):
        """Simulate placing the order and resetting the form."""
        print("Order Placed:")
        print(f"Size: {self.order_details['size']}")
        print(f"Toppings: {', '.join(self.order_details['toppings'])}")
        print(f"Total Price: ${self.order_details['total_price']:.2f}")

        self.controller.reset_order_page()
        self.controller.show_frame("OrderPage")

if __name__ == "__main__":
    app = PizzaApp()
    app.mainloop()
