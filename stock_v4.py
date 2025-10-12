
import tkinter as tk # Importing tkinter for GUI
from tkinter import messagebox, simpledialog # For popups and dialogs
import json # For saving/loading stock data
import os # For file path operations


# Define a custom RoundedButton class that inherits from tk.Canvas to create buttons with rounded corners
class RoundedButton(tk.Canvas):
    # Initialize the RoundedButton with parameters for parent, text, command, font, size, background, and corner radius
    def __init__(self, parent, text, command, font, width, height, bg, corner_radius=10):
        # Calculate approximate pixel width from character width units for better button sizing
        pixel_width = width * 8  # Adjusted for better fit
        # Calculate approximate pixel height from character height units
        pixel_height = height * 20
        # Call the parent Canvas constructor with calculated size, background from parent, and no highlight border
        super().__init__(parent, width=pixel_width, height=pixel_height, bg=parent.cget('bg'), highlightthickness=0)
        # Store the command function to execute when button is clicked
        self.command = command
        # Store the original background color for hover effects
        self.original_bg = bg
        # Set the current background color
        self.bg_color = bg
        # Set the corner radius for rounded corners
        self.radius = corner_radius
        # Store the button text
        self.text = text
        # Store the font for the text
        self.font = font
        # Store the calculated width and height for drawing
        self.w = pixel_width
        self.h = pixel_height
        # Bind left mouse button click to the on_click method
        self.bind("<Button-1>", self.on_click)
        # Bind mouse enter to on_enter for hover effect
        self.bind("<Enter>", self.on_enter)
        # Bind mouse leave to on_leave to reset hover
        self.bind("<Leave>", self.on_leave)
        # Draw the button initially
        self.draw_button()

    # Method to draw the rounded button on the canvas
    def draw_button(self):
        # Get the width and height of the button
        w = self.w
        h = self.h
        # Calculate the corner radius, ensuring it fits within the button size
        r = min(self.radius, min(w, h) // 4)  # Ensure radius fits
        # Clear all previous drawings on the canvas
        self.delete("all")
        # Draw the four corner arcs to create rounded corners
        # Top-left corner arc
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, style=tk.PIESLICE, fill=self.bg_color, outline="")
        # Top-right corner arc
        self.create_arc(w - 2*r, 0, w, 2*r, start=0, extent=90, style=tk.PIESLICE, fill=self.bg_color, outline="")
        # Bottom-left corner arc
        self.create_arc(0, h - 2*r, 2*r, h, start=180, extent=90, style=tk.PIESLICE, fill=self.bg_color, outline="")
        # Bottom-right corner arc
        self.create_arc(w - 2*r, h - 2*r, w, h, start=270, extent=90, style=tk.PIESLICE, fill=self.bg_color, outline="")
        # Draw the horizontal rectangle for the top and bottom middle parts
        self.create_rectangle(r, 0, w - r, h, fill=self.bg_color, outline="")
        # Draw the vertical rectangle for the left and right middle parts
        self.create_rectangle(0, r, w, h - r, fill=self.bg_color, outline="")
        # Draw the button text in the center of the button
        self.create_text(w / 2, h / 2, text=self.text, font=self.font, fill="black")

    # Event handler for mouse click on the button
    def on_click(self, event):
        # If a command is assigned, execute it
        if self.command:
            self.command()

    # Event handler for mouse entering the button area (hover start)
    def on_enter(self, event):
        # Determine hover color based on current background color
        self.bg_color_hover = "#d4edda" if "green" in self.bg_color else "#f8d7da" if "coral" in self.bg_color else "#d1ecf1" if "blue" in self.bg_color else "#fff3cd"
        # Set the background to hover color
        self.bg_color = self.bg_color_hover
        # Redraw the button with new color
        self.draw_button()

    # Event handler for mouse leaving the button area (hover end)
    def on_leave(self, event):
        # Reset background to original color
        self.bg_color = self.original_bg
        # Redraw the button
        self.draw_button()

    # Method to configure button properties dynamically
    def config(self, **kwargs):
        # Update text if provided
        if 'text' in kwargs:
            self.text = kwargs['text']
        # Update font if provided
        if 'font' in kwargs:
            self.font = kwargs['font']
        # Update background color if provided
        if 'bg' in kwargs:
            self.bg_color = kwargs['bg']
            self.original_bg = kwargs['bg']
        # Call parent config method for other properties
        super().config(**kwargs)
        # Redraw the button after changes
        self.draw_button()


# Define the main StockTakingApp class that manages the GUI and stock operations
class StockTakingApp:
    # Main class for the Stock Taking System GUI application.

    # Initialize the StockTakingApp with the root window
    def __init__(self, root):
        # Store the root window reference
        self.root = root
        # Set the window title
        self.root.title("Stock Taking System - Version 4")
        # Set the window size
        self.root.geometry("600x600")
        # Set the background color of the window
        self.root.configure(bg="lightgray")

        # Initialize an empty dictionary to hold stock items and quantities
        self.stock = {}
        # Set the filename for saving/loading stock data
        self.stock_file = "stock_data.json"
        # Set the total capacity for stock
        self.total_capacity = 1000
        # Construct the path to the logo image file
        self.image_path = os.path.join(os.path.dirname(__file__), "company_logo.gif")

        # Load stock data from file at startup
        self.load_stock()

        # Create a frame for the title and logo
        title_frame = tk.Frame(self.root, bg="lightgray")
        title_label = tk.Label(title_frame, text="StockTaker", font=("Arial", 16, "bold"), bg="lightgray")
        title_label.pack()
        # Load and display the company logo if available
        try:
            self.logo_image = tk.PhotoImage(file=self.image_path)
            logo_label = tk.Label(title_frame, image=self.logo_image, bg="lightgray")
            logo_label.pack()
        except tk.TclError:
            # If logo file not found, skip displaying it
            pass
        title_frame.pack(pady=10)

        # Create listbox for displaying stock
        self.stock_listbox = tk.Listbox(self.root, height=15, width=50)
        self.stock_listbox.pack(pady=10)

        # Create buttons frame
        button_frame = tk.Frame(self.root, bg="lightgray")
        button_frame.pack(pady=10)

        # Create add button
        self.add_button = RoundedButton(button_frame, "Add Stock", self.add_stock, ("Arial", 12), 15, 2, "green")
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Create remove button
        self.remove_button = RoundedButton(button_frame, "Remove Stock", self.remove_stock, ("Arial", 12), 15, 2, "coral")
        self.remove_button.pack(side=tk.LEFT, padx=10)

        # Create refresh button
        self.refresh_button = RoundedButton(button_frame, "Refresh", self.refresh_display, ("Arial", 12), 10, 2, "blue")
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        # Create save button
        self.save_button = RoundedButton(button_frame, "Save", self.save_stock, ("Arial", 12), 10, 2, "orange")
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Create status label
        self.status_label = tk.Label(self.root, text="", bg="lightgray", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initial refresh
        self.refresh_display()

    # Method to load stock data from the JSON file
    def load_stock(self):
        # Load stock data from JSON file, coerce quantities to int.
        try:
            # Check if the stock file exists
            if os.path.exists(self.stock_file):
                # Open the file in read mode
                with open(self.stock_file, "r") as file:
                    # Load the JSON data into a dictionary
                    data = json.load(file)
                    # Coerce values to integers to avoid type errors 
                    # Initialize an empty dictionary for cleaned data
                    cleaned = {}
                    # Iterate over each key-value pair in the loaded data
                    for k, v in data.items():
                        try:
                            # Convert the key to string and strip whitespace, value to int
                            cleaned[str(k).strip()] = int(v)
                        except (ValueError, TypeError):
                            # If a value can't be converted to int, skip or set to 0
                            cleaned[str(k).strip()] = 0
                    # Assign the cleaned data to self.stock
                    self.stock = cleaned
                # non-intrusive info (useful while testing)
                # messagebox.showinfo("Load", "Stock data loaded successfully.")
            else:
                # If file doesn't exist, initialize stock as empty dictionary
                self.stock = {}
        except (json.JSONDecodeError, IOError) as error:
            # If there's an error loading the file, show error message and start with empty stock
            messagebox.showerror("Load Error", f"Error loading data: {error}. Starting empty.")
            self.stock = {}

    # Method to save the current stock data to the JSON file
    def save_stock(self):
        # Save current stock data to JSON file
        try:
            # Open the file in write mode
            with open(self.stock_file, "w") as file:
                # Dump the stock dictionary to JSON with indentation for readability
                json.dump(self.stock, file, indent=4)
            # Show success message to the user
            messagebox.showinfo("Save", "Stock data saved successfully.")
        except IOError as error:
            # If there's an error saving, show error message
            messagebox.showerror("Save Error", f"Error saving: {error}")

    # Method to calculate and return the total quantity of all stock items
    def get_total_stock(self):
        # Return total of all stock quantities (int).
        # Sum up all values in the stock dictionary, ensuring they are integers
        return sum(int(q) for q in self.stock.values())

    # Method to refresh the display of stock items in the listbox and update the status label
    def refresh_display(self):
        # Update listbox and status label.
        # Clear all items from the listbox
        self.stock_listbox.delete(0, tk.END)
        # Get the total stock quantity
        total_stock = self.get_total_stock()

        # If there are no stock items, display a message
        if not self.stock:
            self.stock_listbox.insert(tk.END, "No stock items available.")
        else:
            # Sort the stock items alphabetically
            sorted_items = sorted(self.stock.items())
            # Insert each item and quantity into the listbox
            for item, quantity in sorted_items:
                self.stock_listbox.insert(tk.END, f"{item}: {quantity}")

        # Calculate remaining capacity
        remaining = self.total_capacity - total_stock
        # Determine color based on remaining capacity
        if remaining < 0:
            remaining = 0
            color = "red"
        elif remaining < 100:
            color = "orange"
        else:
            color = "green"

        # Create status text with total stock and remaining capacity
        status_text = f"Total Stock: {total_stock}/{self.total_capacity} (Remaining: {remaining})"
        # Update the status label with the text and color
        self.status_label.config(text=status_text, fg=color)

    # Method to prompt the user to add stock items, validate input, and enforce capacity limits
    def add_stock(self):
        # Prompt user to add stock. Validates input and enforces capacity boundary."""
        try:
            # Prompt the user for the item name
            item_name = simpledialog.askstring("Input", "Enter stock item name:")
            # If user cancelled, return
            if item_name is None:
                return  # user cancelled
            # Strip whitespace from item name
            item_name = item_name.strip()
            # Check if item name is empty
            if not item_name:
                messagebox.showerror("Input Error", "Item name cannot be empty.")
                return

            # Get the current total stock
            current_total = self.get_total_stock()
            # Prompt the user for the quantity to add
            quantity = simpledialog.askinteger("Input", "Enter quantity to add:")
            # If user cancelled, return
            if quantity is None:
                return  # cancelled
            # Check if quantity is positive
            if quantity <= 0:
                messagebox.showerror("Input Error", "Quantity must be a positive integer.")
                return

            # Check if adding this quantity would exceed capacity
            if current_total + quantity > self.total_capacity:
                # Calculate maximum quantity that can be added
                max_add = self.total_capacity - current_total
                messagebox.showwarning(
                    "Capacity Warning",
                    f"Adding {quantity} would exceed capacity ({self.total_capacity}). Max add: {max_add}.",
                )
                return

            # Add or increment the item in the stock dictionary
            self.stock[item_name] = self.stock.get(item_name, 0) + int(quantity)
            # Show success message
            messagebox.showinfo("Success", f"Added {quantity} of '{item_name}'.")
            # Auto-save and refresh
            try:
                # Attempt to save the stock data
                self.save_stock()
            except Exception:
                # save_stock already handles its own errors; we proceed to refresh anyway.
                pass
            # Refresh the display to show updated stock
            self.refresh_display()
        except Exception as e:
            # Show error message for any unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Method to prompt the user to remove stock items, using selection if available or asking for item name
    def remove_stock(self):
        #Prompt user to remove stock. Use selection if available, else ask for item name."""
        try:
            # If user has selected a listbox item, try to parse it (format "Name: qty")
            sel = self.stock_listbox.curselection()
            item_name = None
            if sel:
                selected_text = self.stock_listbox.get(sel[0])
                if ":" in selected_text:
                    item_name = selected_text.split(":", 1)[0].strip()
                elif selected_text == "No stock items available.":
                    messagebox.showinfo("Remove Stock", "No items to remove.")
                    return

            if not item_name:
                # Ask for item name explicitly if nothing selected
                item_name = simpledialog.askstring("Input", "Enter stock item name to remove:")
                if item_name is None:
                    return
                item_name = item_name.strip()
                if not item_name:
                    messagebox.showerror("Input Error", "Item name cannot be empty.")
                    return

            if item_name not in self.stock:
                messagebox.showerror("Not Found", f"Item '{item_name}' not found in stock.")
                return

            current_qty = int(self.stock[item_name])
            # Ask how many to remove
            quantity = simpledialog.askinteger(
                "Input", f"Enter quantity to remove (current: {current_qty}).\nEnter {current_qty} to remove all:"
            )
            if quantity is None:
                return
            if quantity <= 0:
                messagebox.showerror("Input Error", "Quantity must be a positive integer.")
                return

            if quantity >= current_qty:
                # Remove the item entirely
                del self.stock[item_name]
                messagebox.showinfo("Removed", f"Removed all of '{item_name}'.")
            else:
                # Subtract quantity
                self.stock[item_name] = current_qty - int(quantity)
                messagebox.showinfo("Removed", f"Removed {quantity} of '{item_name}'. Remaining: {self.stock[item_name]}")

            # Auto-save and refresh
            try:
                self.save_stock()
            except Exception:
                pass
            self.refresh_display()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Method to handle the window closing event, auto-saving stock data before destroying the root window
    def on_closing(self):
        #Auto-save on window close, then destroy root.
        try:
            # Attempt to save silently (don't spam user with error on close)
            with open(self.stock_file, "w") as file:
                json.dump(self.stock, file, indent=4)
        except Exception:
            # If save fails, still attempt to close gracefully after informing user.
            messagebox.showwarning("Save Warning", "Could not save stock data on exit.")
        finally:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTakingApp(root)
    root.mainloop()
