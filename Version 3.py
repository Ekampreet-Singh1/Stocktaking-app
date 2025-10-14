# Stock Taking System - Version 3

import tkinter as tk  # Importing tkinter for GUI
from tkinter import messagebox, simpledialog  # For popups and input dialogs
import json  # For saving and loading data as JSON files
import os  # For checking if files exist

# This is a class
class StockTakingApp:
    def __init__(self, root):
        self.root = root  # This is an attribute
        self.root.title("Stock Taking System - Version 3")  # Setting the window title
        self.root.geometry("500x500")  # Larger window for the Listbox

        self.stock = {}  # This is an attribute (dictionary for stock items)
        self.stock_file = "stock_data.json"  # File to save stock data

        # Load stock from file when starting up
        self.load_stock()

        # Title frame for better organization
        title_frame = tk.Frame(root)
        title_frame.pack(pady=10)

        # Title label with font
        self.title_label = tk.Label(title_frame, text="Stock Taking System v3", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0)

        # Buttons frame for organization
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)

        # Add button with styling
        self.add_button = tk.Button(buttons_frame, text="Add Stock Item", command=self.add_stock, 
                                    font=("Arial", 11), width=15, height=1, bg="lightgreen")
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        # Remove button with styling
        self.remove_button = tk.Button(buttons_frame, text="Remove Stock Quantity", command=self.remove_stock, 
                                       font=("Arial", 11), width=15, height=1, bg="lightcoral")
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)

        # Save button (new)
        self.save_button = tk.Button(buttons_frame, text="Save Stock", command=self.save_stock, 
                                     font=("Arial", 11), width=15, height=1, bg="lightblue")
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        # Refresh button (new)
        self.refresh_button = tk.Button(buttons_frame, text="Refresh View", command=self.refresh_display, 
                                        font=("Arial", 11), width=15, height=1, bg="lightyellow")
        self.refresh_button.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

        # Display frame for Listbox
        display_frame = tk.Frame(root)
        display_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Label for Listbox
        list_label = tk.Label(display_frame, text="Current Stock Items:", font=("Arial", 10, "bold"))
        list_label.pack(anchor=tk.W)

        # Frame for Listbox and scrollbar
        listbox_frame = tk.Frame(display_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox to show stock (new feature)
        self.stock_listbox = tk.Listbox(listbox_frame, font=("Arial", 10), height=15, width=50)
        
        # Scrollbar for Listbox
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.stock_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.stock_listbox.yview)
        self.stock_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Update the Listbox on start
        self.refresh_display()

        # Save on close (new)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # This is a method (loads stock from JSON file)
    def load_stock(self):
        try:
            if os.path.exists(self.stock_file):  # Check if file exists
                with open(self.stock_file, 'r') as file:
                    self.stock = json.load(file)  # Load the dictionary
                messagebox.showinfo("Load", "Stock data loaded from file.")
            else:
                self.stock = {}  # Start empty if no file
        except (json.JSONDecodeError, IOError) as e:  # Handle file errors
            messagebox.showerror("Load Error", f"Error loading stock data: {e}\nStarting with empty stock.")
            self.stock = {}

    # This is a method (saves stock to JSON file)
    def save_stock(self):
        try:
            with open(self.stock_file, 'w') as file:
                json.dump(self.stock, file, indent=4)  # Save as formatted JSON
            messagebox.showinfo("Save", "Stock data saved to file.")
        except IOError as e:  # Handle save errors
            messagebox.showerror("Save Error", f"Error saving stock data: {e}")

    # This is a method (updates the Listbox display)
    def refresh_display(self):
        self.stock_listbox.delete(0, tk.END)  # Clear Listbox
        if not self.stock:
            self.stock_listbox.insert(tk.END, "No stock items available.")
        else:
            sorted_items = sorted(self.stock.items())  # Sort for display
            for item, quantity in sorted_items:
                self.stock_listbox.insert(tk.END, f"{item}: {quantity}")

    # This is a method (used to add items to stock - with validation and refresh)
    def add_stock(self):
        try:
            item_name = simpledialog.askstring("Input", "Enter stock item name:")
            if item_name:
                item_name = item_name.strip()  # Clean up spaces
                if not item_name:
                    raise ValueError("Item name cannot be empty.")
                quantity = simpledialog.askinteger("Input", "Enter quantity to add:")
                if quantity is not None and quantity > 0:
                    self.stock[item_name] = self.stock.get(item_name, 0) + quantity  # Update stock
                    messagebox.showinfo("Success", f"Added {quantity} of '{item_name}' to stock.")
                    self.refresh_display()  # Update Listbox
                else:
                    messagebox.showwarning("Error", "Please enter a valid positive quantity.")
        except ValueError as e:  # Handle input errors
            messagebox.showerror("Input Error", str(e))

    # This is a method (used to view stock - now uses Listbox)
    def view_stock(self):
        self.refresh_display()
        messagebox.showinfo("View", "Check the Listbox for current stock items.")

    # This is a method (used to remove quantity from stock - with validation and refresh)
    def remove_stock(self):
        try:
            item_name = simpledialog.askstring("Input", "Enter stock item name to remove from:")
            if item_name:
                item_name = item_name.strip()  # Clean up spaces
                if item_name in self.stock:
                    current_quantity = self.stock[item_name]
                    quantity_to_remove = simpledialog.askinteger("Input", f"Current quantity: {current_quantity}\nEnter quantity to remove:")
                    if quantity_to_remove is not None and quantity_to_remove > 0:
                        if quantity_to_remove > current_quantity:
                            messagebox.showwarning("Warning", f"Only {current_quantity} available. Removing all.")
                            self.stock[item_name] = 0
                        else:
                            self.stock[item_name] -= quantity_to_remove
                        if self.stock[item_name] == 0:
                            del self.stock[item_name]  # Remove if zero
                        messagebox.showinfo("Success", f"Removed {quantity_to_remove} of '{item_name}' from stock.")
                        self.refresh_display()  # Update Listbox
                    else:
                        messagebox.showwarning("Error", "Please enter a valid positive quantity.")
                else:
                    messagebox.showwarning("Error", f"'{item_name}' not found in stock.")
        except ValueError as e:  # Handle input errors
            messagebox.showerror("Input Error", str(e))

    # This is a method (handles closing the window - saves first)
    def on_closing(self):
        self.save_stock()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Creates a main window
    app = StockTakingApp(root)
    root.mainloop()  # Starts the GUI event loop
