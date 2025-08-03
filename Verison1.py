#THis is a stocktaking system
import tkinter as tk  # Importing tkinter for GUI
from tkinter import messagebox, simpledialog 

# This is a class
class StockTakingApp:
    def __init__(self, root):
        self.root = root  # This is an attribute
        self.root.title("Stock Taking System")  # Setting the window title

        self.stock = {}  # This is an attribute (a dictionary to store stock items)

        # This is an attribute (a Label object)
        self.label = tk.Label(root, text="Stock Taking System", font=("Arial", 16))
        self.label.pack(pady=10)  # This is a method call to place the label

        # This is an attribute (a Button object)
        self.add_button = tk.Button(root, text="Add Stock Item", command=self.add_stock)
        self.add_button.pack(pady=5)  # This is a method

        # This is an attribute (a Button object)
        self.view_button = tk.Button(root, text="View Stock Items", command=self.view_stock)
        self.view_button.pack(pady=5)  # This is a method

        # This is an attribute (a Button object)
        self.delete_button = tk.Button(root, text="Delete Stock Item", command=self.delete_stock)
        self.delete_button.pack(pady=5)  # This is a method

    # This is a method (used to add items to stock)
    def add_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name:")  # Ask user for item name
        if item_name:
            quantity = simpledialog.askinteger("Input", "Enter quantity:")  # Ask user for quantity
            if quantity is not None:
                self.stock[item_name] = self.stock.get(item_name, 0) + quantity  # Update stock dictionary
                messagebox.showinfo("Success", f"Added {quantity} of {item_name} to stock.")  # Show what action has happened

    # This is a method (used to view current stock items)
    def view_stock(self):
        if not self.stock:
            messagebox.showinfo("Stock Items", "No stock items available.")  # Show if stock is empty
            return
        stock_items = "\n".join([f"{item}: {quantity}" for item, quantity in self.stock.items()])  # Format stock list
        messagebox.showinfo("Stock Items", stock_items)  # Show stock items

    # This is a method (used to delete a stock item)
    def delete_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name to delete:")  # Ask for item name to delete
        if item_name in self.stock:
            del self.stock[item_name]  # Delete the item from the dictionary
            messagebox.showinfo("Success", f"Deleted {item_name} from stock.")  # Confirmation  to let user know what is happening
        else:
            messagebox.showwarning("Error", f"{item_name} not found in stock.")  # Show error if item not found

if __name__ == "__main__":
    root = tk.Tk()  
    app = StockTakingApp(root)  
    root.mainloop()  
