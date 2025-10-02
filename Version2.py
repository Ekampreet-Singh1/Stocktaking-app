# Stock Taking System - Version 2
import tkinter as tk  # Importing tkinter for GUI
from tkinter import messagebox, simpledialog

# This is a class
class StockTakingApp:
    def __init__(self, root):
        self.root = root  # This is an attribute
        self.root.title("Stock Taking System")  # Setting the window title
        self.root.geometry("350x300")  # Set a fixed window size for better layout

        self.stock = {}  # This is an attribute (a dictionary to store stock items)

        # Title frame for better organization
        title_frame = tk.Frame(root)
        title_frame.pack(pady=20)

        # Title label with improved font
        self.label = tk.Label(title_frame, text="Stock Taking System", font=("Arial", 18, "bold"))
        self.label.grid(row=0, column=0)

        # Buttons frame for organization
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=20)

        # Add button with styling
        self.add_button = tk.Button(buttons_frame, text="Add Stock Item", command=self.add_stock, 
                                    font=("Arial", 12), width=18, height=2)
        self.add_button.grid(row=0, column=0, padx=10, pady=5)

        # View button with styling
        self.view_button = tk.Button(buttons_frame, text="View Stock Items", command=self.view_stock, 
                                     font=("Arial", 12), width=18, height=2)
        self.view_button.grid(row=1, column=0, padx=10, pady=5)

        # Remove button (improved from delete) with styling
        self.remove_button = tk.Button(buttons_frame, text="Remove Stock Quantity", command=self.remove_stock, 
                                       font=("Arial", 12), width=18, height=2)
        self.remove_button.grid(row=2, column=0, padx=10, pady=5)

    # This is a method (used to add items to stock - uses popups like version 1)
    def add_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name:")  # Popup for item name
        if item_name:
            quantity = simpledialog.askinteger("Input", "Enter quantity to add:")  # Popup for quantity
            if quantity is not None and quantity > 0:
                self.stock[item_name] = self.stock.get(item_name, 0) + quantity  # Update stock dictionary
                messagebox.showinfo("Success", f"Added {quantity} of '{item_name}' to stock.")  # Success popup
            else:
                messagebox.showwarning("Error", "Please enter a valid positive quantity.")

    # This is a method (used to view current stock items - uses popup like version 1)
    def view_stock(self):
        if not self.stock:
            messagebox.showinfo("Stock Items", "No stock items available.")  # Empty stock popup
            return
        stock_items = "\n".join([f"{item}: {quantity}" for item, quantity in sorted(self.stock.items())])  # Format sorted list
        messagebox.showinfo("Stock Items", stock_items)  # Show stock in popup

    # This is a method (improved from delete: used to remove a quantity from stock - uses popups like version 1)
    def remove_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name to remove from:")  # Popup for item name
        if item_name and item_name in self.stock:
            current_quantity = self.stock[item_name]
            quantity_to_remove = simpledialog.askinteger("Input", f"Current quantity: {current_quantity}\nEnter quantity to remove:")  # Popup for quantity to remove
            if quantity_to_remove is not None and quantity_to_remove > 0:
                if quantity_to_remove > current_quantity:
                    messagebox.showwarning("Warning", f"Only {current_quantity} available. Removing all.")
                    self.stock[item_name] = 0  # Set to 0 if exceeds
                    if self.stock[item_name] == 0:
                        del self.stock[item_name]  # Remove item if quantity reaches 0
                else:
                    self.stock[item_name] -= quantity_to_remove  # Subtract quantity
                    if self.stock[item_name] == 0:
                        del self.stock[item_name]  # Remove item if quantity reaches 0
                messagebox.showinfo("Success", f"Removed {quantity_to_remove} of '{item_name}' from stock.")  # Success popup
            else:
                messagebox.showwarning("Error", "Please enter a valid positive quantity.")
        elif item_name:
            messagebox.showwarning("Error", f"'{item_name}' not found in stock.")  # Error if item not found

if __name__ == "__main__":
    root = tk.Tk()  # Creates a main window
    app = StockTakingApp(root)
    root.mainloop()  # Starts the GUI event loop
