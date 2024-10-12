import tkinter as tk  # Importing tkinter for GUI creation
from tkinter import ttk  # Importing themed tkinter widgets
from tkinter import messagebox  # Importing messagebox for warnings and confirmations
from PIL import Image, ImageTk  # Importing for image handling
import os  # Importing to handle file paths

class PizzaApp(tk.Tk):
    """
    This class represents the main window of the Pizza Ordering App.
    """
    def __init__(self):
        super().__init__()
        self.title("Pizza Ordering App")  # Set window title
        self.geometry("800x800")  # Set window size
        self.configure(bg="#2e2e2e")  # Set background color to dark theme
        
        # Paths to images
        pizza_image_path = "bag.png"  # Pizza image for summary page
        logo_image_path = "logo.png"  # Logo image for order page
        
        # Load and resize images to fit in the UI
        self.img_pizza = self.load_image(pizza_image_path, "An image of a shopping bag", (200, 200))  # Load pizza image (200x200)
        self.img_logo = self.load_image(logo_image_path, "An image of Home Fire Pizza's logo", (200, 200))  # Load logo image (200x200)

        # Create container frame to hold different pages
        container = tk.Frame(self, bg="#2e2e2e")
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to store all frames (OrderPage and SummaryPage)
        self.frames = {}
        for F in (OrderPage, SummaryPage):
            page_name = F.__name__  # Name of page
            frame = F(parent=container, controller=self)  # Create instance of the page
            self.frames[page_name] = frame  # Add frame to the dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Stack all pages on top of each other
        
        self.show_frame("OrderPage")  # Show first page (OrderPage)

    def load_image(self, img_path, alt_text, size=None):
        """
        Load image from the given path, resize if specified.
        If an error occurs, print a message and return None.
        """
        try:
            image = Image.open(img_path)  # Load image from file
            if size:
                image = image.resize(size)  # Resize image if size is provided
            return ImageTk.PhotoImage(image)  # Convert to PhotoImage for tkinter
        except Exception as e:
            print(f"Error loading image {alt_text}: {e}")  # Print error message
            return None  # Return None if loading fails

    def show_frame(self, page_name):
        """
        Show frame (page) specified by page_name by bringing it to the front.
        """
        frame = self.frames[page_name]  # Get frame object from the dictionary
        frame.tkraise()  # Bring frame to the front

    def log_order(self, order_details):
        """
        Pass order details to summary page and switch to the SummaryPage.
        """
        summary_frame = self.frames["SummaryPage"]  # Get summary page frame
        summary_frame.display_summary(order_details)  # Call method to display order details
        self.show_frame("SummaryPage")  # Switch to summary page

    def reset_order_page(self):
        """
        Reset order form on the OrderPage to its default state.
        """
        order_page = self.frames["OrderPage"]  # Get order page frame
        order_page.reset_order()  # Call reset method


class OrderPage(tk.Frame):
    """
    This class represents the Order Page, where users can select pizza size, and toppings.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Reference to the main app (controller)
        self.configure(bg="#2e2e2e")  # Set background color to dark theme

        # Center frame to hold widgets
        center_frame = tk.Frame(self, bg="#2e2e2e")
        center_frame.pack(expand=True)

        # Title label
        title_label = tk.Label(center_frame, text="Welcome to Home Fire Pizza!", font=("Helvetica", 20), bg="#2e2e2e", fg="#f5e6ca")
        title_label.pack(pady=20)

        # Display logo image if loaded successfully
        if controller.img_logo:
            logo_label = tk.Label(center_frame, image=controller.img_logo, bg="#2e2e2e")
            logo_label.image = controller.img_logo  # Prevent image garbage collection
            logo_label.pack(pady=10)

        # Label and dropdown for selecting pizza size
        self.size_label = tk.Label(center_frame, text="Select Pizza Size:", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca")
        self.size_label.pack(pady=5)
        self.size_var = tk.StringVar(value="Medium")  # Default size is Medium
        self.size_dropdown = ttk.Combobox(center_frame, textvariable=self.size_var, values=["Small", "Medium", "Large"], state="readonly")
        self.size_dropdown.pack(pady=5)

        # Label and listbox for selecting toppings
        self.toppings_label = tk.Label(center_frame, text="Select Toppings:", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca")
        self.toppings_label.pack(pady=5)
        self.toppings_listbox = tk.Listbox(center_frame, selectmode="multiple", height=6, bg="#3e3e3e", fg="#f5e6ca", selectbackground="#5e5e5e")
        toppings = ["Cheese", "Pepperoni", "Mushrooms", "Onions", "Sausage", "Bacon", "Green Peppers", "Olives"]
        for topping in toppings:
            self.toppings_listbox.insert(tk.END, topping)  # Add toppings to listbox
        self.toppings_listbox.pack(pady=5)

        # Button to confirm order
        self.confirm_button = ttk.Button(center_frame, text="Confirm Order", command=self.confirm_order)
        self.confirm_button.pack(pady=20)

        # Button to exit the app
        self.exit_button = ttk.Button(center_frame, text="Exit", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def confirm_order(self):
        """
        Handle order confirmation, calculate total price, and pass data to the summary page.
        """
        size = self.size_var.get()  # Get selected pizza size
        selected_toppings = [self.toppings_listbox.get(i) for i in self.toppings_listbox.curselection()]  # Get selected toppings

        if not selected_toppings:
            messagebox.showwarning("Warning", "Please select at least one topping.")  # Show warning if no toppings selected
            return

        # Pricing logic
        size_prices = {"Small": 8, "Medium": 10, "Large": 12}
        total_price = size_prices.get(size, 0) + (1.5 * len(selected_toppings))  # Calculate total price

        # Store order details in dictionary
        order_details = {
            "size": size,
            "toppings": selected_toppings,
            "total_price": total_price
        }

        self.controller.log_order(order_details)  # Log and move to summary page

    def reset_order(self):
        """
        Reset order form to its default state.
        """
        self.size_var.set("Medium")  # Reset pizza size to Medium
        self.toppings_listbox.selection_clear(0, tk.END)  # Clear toppings selection

    def exit_app(self):
        """
        Handle exit process, ask for confirmation before closing the app.
        """
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):  # Confirmation dialog
            self.controller.destroy()  # Close app if confirmed


class SummaryPage(tk.Frame):
    """
    This class represents the Summary Page. where the user can see their order summary.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Reference to the main app (controller)
        self.configure(bg="#2e2e2e")  # Set background color to dark theme

        # Center frame to hold widgets
        center_frame = tk.Frame(self, bg="#2e2e2e")
        center_frame.pack(expand=True)

        # Display shopping bag image if loaded successfully
        if controller.img_pizza:
            pizza_label = tk.Label(center_frame, image=controller.img_pizza, bg="#2e2e2e")
            pizza_label.image = controller.img_pizza  # Prevent image garbage collection
            pizza_label.pack(pady=10)

        # Title label for order summary
        summary_title = tk.Label(center_frame, text="Order Summary", font=("Helvetica", 20), bg="#2e2e2e", fg="#f5e6ca")
        summary_title.pack(pady=20)

        # Label to display order details (size, toppings, total price)
        self.summary_label = tk.Label(center_frame, text="", font=("Helvetica", 14), bg="#2e2e2e", fg="#f5e6ca", justify="left")
        self.summary_label.pack(pady=10)

        # Button to place order
        self.place_order_button = ttk.Button(center_frame, text="Place Order", command=self.place_order)
        self.place_order_button.pack(pady=10)

        # Button to go back to the order page
        self.back_button = ttk.Button(center_frame, text="Back to Order", command=lambda: controller.show_frame("OrderPage"))
        self.back_button.pack(pady=5)

    def display_summary(self, order_details):
        """
        Display order summary (size, toppings, total price).
        """
        self.order_details = order_details  # Store order details
        summary_text = (
            f"Size: {order_details['size']}\n"
            f"Toppings: {', '.join(order_details['toppings'])}\n"
            f"Total Price: ${order_details['total_price']:.2f}"  # Format price to 2 decimal places
        )
        self.summary_label.config(text=summary_text)  # Update summary label with order details

    def place_order(self):
        """
        Simulate placing order and reset the form for new order.
        """
        # Print  order details (simulation of order placement)
        print("Order Placed:")
        print(f"Size: {self.order_details['size']}")
        print(f"Toppings: {', '.join(self.order_details['toppings'])}")
        print(f"Total Price: ${self.order_details['total_price']:.2f}")

        self.controller.reset_order_page()  # Reset order page
        self.controller.show_frame("OrderPage")  # Go back to order page


if __name__ == "__main__":
    app = PizzaApp()  # Create instance of the app
    app.mainloop()  # Start the main event loop
