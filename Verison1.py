import tkinter as tk
from tkinter import messagebox, simpledialog

class StockTakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Taking System")

        self.stock = {}

        self.label = tk.Label(root, text="Stock Taking System", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Stock Item", command=self.add_stock)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Stock Items", command=self.view_stock)
        self.view_button.pack(pady=5)
        
        self.delete_button = tk.Button(root, text="Delete Stock Item", command=self.delete_stock)
        self.delete_button.pack(pady=5)

    def add_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name:")
        if item_name:
            quantity = simpledialog.askinteger("Input", "Enter quantity:")
            if quantity is not None:
                self.stock[item_name] = self.stock.get(item_name, 0) + quantity
                messagebox.showinfo("Success", f"Added {quantity} of {item_name} to stock.")

    def view_stock(self):
        if not self.stock:
            messagebox.showinfo("Stock Items", "No stock items available.")
            return
        stock_items = "\n".join([f"{item}: {quantity}" for item, quantity in self.stock.items()])
        messagebox.showinfo("Stock Items", stock_items)

    def delete_stock(self):
        item_name = simpledialog.askstring("Input", "Enter stock item name to delete:")
        if item_name in self.stock:
            del self.stock[item_name]
            messagebox.showinfo("Success", f"Deleted {item_name} from stock.")
        else:
            messagebox.showwarning("Error", f"{item_name} not found in stock.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTakingApp(root)
    root.mainloop()
