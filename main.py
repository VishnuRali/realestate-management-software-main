import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from app import RealEstateApp
from seed_data import seed_database
import os
import sqlite3

class LoginApp:
    def __init__(self, root):
        """Initialize the login application"""
        self.root = root
        self.db = Database("real_estate.db")
        self.current_user = None
        self.configure_window()
        self.create_users_table()
        self.login_screen()

    def configure_window(self):
        """Configure the main window"""
        self.root.title("Real Estate Management System - Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

    def create_users_table(self):
        """Create the users table if it doesn't exist"""
        self.db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                mobile TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        self.db.conn.commit()

    def clear(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        """Display the login screen"""
        self.clear()
        tk.Label(self.root, text="Real Estate Listings", font=("Arial", 22, "bold")).pack(pady=20)
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Label(frame, text="Mobile").grid(row=0, column=0)
        self.mobile_entry = tk.Entry(frame)
        self.mobile_entry.grid(row=0, column=1)
        tk.Label(frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1)

        def login():
            """Handle login logic"""
            mobile = self.mobile_entry.get()
            password = self.password_entry.get()
            self.db.cursor.execute("SELECT * FROM users WHERE mobile=? AND password=?", (mobile, password))
            if self.db.cursor.fetchone():
                self.current_user = mobile
                self.start_main_app()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        ttk.Button(frame, text="Login", command=login).grid(row=2, columnspan=2, pady=10)
        ttk.Button(self.root, text="Register", command=self.register_screen).pack(pady=5)

    def register_screen(self):
        """Display the registration screen"""
        self.clear()
        tk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)
        frame = tk.Frame(self.root)
        frame.pack()
        labels = ["Name", "Address", "Mobile", "Password", "Re-enter Password"]
        self.entries = []
        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i, column=0)
            entry = tk.Entry(frame, show="*" if "Password" in label else None)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        def register():
            """Handle registration logic"""
            name, address, mobile, pwd, repwd = [e.get() for e in self.entries]
            if pwd != repwd:
                messagebox.showerror("Error", "Passwords do not match")
                return
            try:
                self.db.cursor.execute("INSERT INTO users (name, address, mobile, password) VALUES (?, ?, ?, ?)", (name, address, mobile, pwd))
                self.db.conn.commit()
                messagebox.showinfo("Success", "Registered successfully!")
                self.login_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Mobile number already registered")

        ttk.Button(frame, text="Register", command=register).grid(row=5, columnspan=2, pady=10)

    def start_main_app(self):
        """Start the main application after successful login"""
        self.root.destroy()  # Close the login window
        root = tk.Tk()  # Create a new root window for the main application
        app = RealEstateApp(root, self.db)  # Initialize the main application
        root.mainloop()  # Run the main application

def main():
    # Check if database exists, if not, create and seed it
    if not os.path.exists("real_estate.db"):
        print("Database not found. Creating and seeding with sample data...")
        seed_database()
    else:
        # Check if database is empty
        db = Database("real_estate.db")
        try:
            db.cursor.execute("SELECT COUNT(*) FROM properties")
            property_count = db.cursor.fetchone()[0]

            db.cursor.execute("SELECT COUNT(*) FROM agents")
            agent_count = db.cursor.fetchone()[0]

            db.cursor.execute("SELECT COUNT(*) FROM inquiries")
            inquiry_count = db.cursor.fetchone()[0]

            db.cursor.execute("SELECT COUNT(*) FROM marketing")
            marketing_count = db.cursor.fetchone()[0]

            if property_count == 0 and agent_count == 0 and inquiry_count == 0 and marketing_count == 0:
                print("Database is empty. Seeding with sample data...")
                db.close()  # Close the connection before seeding
                seed_database()
            else:
                db.close()  # Close the connection
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            print("Recreating the database...")
            db.close()  # Ensure the connection is closed before deleting the file
            os.remove("real_estate.db")
            seed_database()

    # Initialize the root window for login
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()