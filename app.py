import tkinter as tk
from tkinter import ttk, messagebox

from property import PropertyTab
from agent import AgentTab
from inquiry import InquiryTab
from marketing import MarketingTab # Import the marketing tab

class RealEstateApp:
    def __init__(self, root, database):
        """Initialize the main application"""
        self.root = root
        self.db = database

        # Configure the main window
        self.root.title("Real Estate Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        # Set application style
        self.configure_styles()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize tabs
        self.property_tab = PropertyTab(self.notebook, self.db, self)
        self.agent_tab = AgentTab(self.notebook, self.db, self)
        self.inquiry_tab = InquiryTab(self.notebook, self.db, self)
        self.marketing_tab = MarketingTab(self.notebook, self.db, self)  # Add this line

        # Add a status bar
        self.create_status_bar()

    def configure_styles(self):
        """Configure the application styles"""
        self.style = ttk.Style()

        # Configure frame style
        self.style.configure("TFrame", background="#f0f0f0")

        # Configure button style
        self.style.configure(
            "TButton",
            background="#4CAF50",
            foreground="black",
            font=("Arial", 10, "bold"),
            padding=5,
        )
        self.style.map(
            "TButton",
            background=[("active", "#45a049"), ("pressed", "#2e7d32")],
            relief=[("pressed", "sunken")],
        )

        # Configure label style
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 11))

        # Configure heading style
        self.style.configure("Heading.TLabel", font=("Arial", 14, "bold"))

        # Configure notebook style
        self.style.configure("TNotebook", background="#f0f0f0", tabposition="n")
        self.style.configure(
            "TNotebook.Tab", background="#d0d0d0", padding=[10, 2], font=("Arial", 10)
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "#4CAF50"), ("active", "#80c883")],
            foreground=[("selected", "white"), ("active", "black")],
        )

        # Configure treeview style
        self.style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=25,
            fieldbackground="white",
            font=("Arial", 10),
        )
        self.style.configure(
            "Treeview.Heading", font=("Arial", 10, "bold"), background="#d0d0d0"
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#4CAF50")],
            foreground=[("selected", "white")],
        )

    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN, padding=(10, 2))
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(
            status_frame, textvariable=self.status_var, anchor=tk.W
        )
        status_label.pack(side=tk.LEFT)

        # Add a quit button to the status bar
        quit_button = ttk.Button(status_frame, text="Quit", command=self.root.destroy)
        quit_button.pack(side=tk.RIGHT, padx=5)

    def set_status(self, message):
        """Set the status bar message"""
        self.status_var.set(message)