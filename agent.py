import tkinter as tk
from tkinter import ttk, messagebox


class AgentTab:
    def __init__(self, parent, database, app):
        """Initialize the Agent Registration tab"""
        self.parent = parent
        self.db = database
        self.app = app

        # Variables for entry fields
        self.agent_name_var = tk.StringVar()
        self.agent_phone_var = tk.StringVar()
        self.agent_email_var = tk.StringVar()
        self.agent_license_var = tk.StringVar()
        self.agent_commission_var = tk.StringVar()
        self.agent_search_var = tk.StringVar()

        # Create the tab UI
        self.create_tab()

    def create_tab(self):
        """Create the Agent Registration tab UI"""
        agent_frame = ttk.Frame(self.parent)
        self.parent.add(agent_frame, text="Agent Registration")

        # Left frame for agent entry
        left_frame = ttk.Frame(agent_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for agent listing
        right_frame = ttk.Frame(agent_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Agent input fields
        ttk.Label(
            left_frame, text="Agent Registration", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(left_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(left_frame, textvariable=self.agent_name_var, width=30).grid(
            row=1, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(left_frame, textvariable=self.agent_phone_var, width=15).grid(
            row=2, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(left_frame, textvariable=self.agent_email_var, width=30).grid(
            row=3, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="License Number:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(left_frame, textvariable=self.agent_license_var, width=15).grid(
            row=4, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Commission Rate (%):").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        ttk.Spinbox(
            left_frame,
            from_=0,
            to=10,
            increment=0.5,
            textvariable=self.agent_commission_var,
            width=5,
        ).grid(row=5, column=1, pady=5, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Agent", command=self.add_agent).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Update Agent", command=self.update_agent).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Delete Agent", command=self.delete_agent).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(
            side=tk.LEFT, padx=5
        )

        # Agent listing
        ttk.Label(right_frame, text="Agent Directory", font=("Arial", 14, "bold")).pack(
            pady=10
        )

        # Search frame
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(search_frame, textvariable=self.agent_search_var, width=20).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Search", command=self.search_agents).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Show All", command=self.load_agents).pack(
            side=tk.LEFT, padx=5
        )

        # Treeview for agent listing
        columns = ("id", "name", "phone", "email", "license", "join_date", "commission")
        self.agent_tree = ttk.Treeview(
            right_frame, columns=columns, show="headings", height=15
        )

        # Define headings
        self.agent_tree.heading("id", text="ID")
        self.agent_tree.heading("name", text="Name")
        self.agent_tree.heading("phone", text="Phone")
        self.agent_tree.heading("email", text="Email")
        self.agent_tree.heading("license", text="License #")
        self.agent_tree.heading("join_date", text="Join Date")
        self.agent_tree.heading("commission", text="Commission %")

        # Define columns
        self.agent_tree.column("id", width=40)
        self.agent_tree.column("name", width=150)
        self.agent_tree.column("phone", width=100)
        self.agent_tree.column("email", width=150)
        self.agent_tree.column("license", width=80)
        self.agent_tree.column("join_date", width=100)
        self.agent_tree.column("commission", width=100)

        # Add scrollbar
        agent_scrollbar = ttk.Scrollbar(
            right_frame, orient=tk.VERTICAL, command=self.agent_tree.yview
        )
        self.agent_tree.configure(yscrollcommand=agent_scrollbar.set)

        # Pack tree and scrollbar
        self.agent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        agent_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind select event
        self.agent_tree.bind("<<TreeviewSelect>>", self.agent_selected)

        # Load data
        self.load_agents()

    def add_agent(self):
        """Add a new agent to the database"""
        name = self.agent_name_var.get()
        phone = self.agent_phone_var.get()
        email = self.agent_email_var.get()
        license_number = self.agent_license_var.get()
        commission_rate = self.agent_commission_var.get()

        if not name:
            messagebox.showerror("Error", "Agent Name is a required field")
            return

        try:
            commission_rate = float(commission_rate) if commission_rate else 0

            self.db.add_agent(name, phone, email, license_number, commission_rate)
            self.clear_fields()
            self.load_agents()

            # Update comboboxes in other tabs
            self.app.property_tab.update_agent_combo()
            self.app.inquiry_tab.update_agent_combo()

            messagebox.showinfo("Success", "Agent added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_agent(self):
        """Update an existing agent in the database"""
        selected_item = self.agent_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an agent to update")
            return

        agent_id = self.agent_tree.item(selected_item, "values")[0]
        name = self.agent_name_var.get()
        phone = self.agent_phone_var.get()
        email = self.agent_email_var.get()
        license_number = self.agent_license_var.get()
        commission_rate = self.agent_commission_var.get()

        if not name:
            messagebox.showerror("Error", "Agent Name is a required field")
            return

        try:
            commission_rate = float(commission_rate) if commission_rate else 0

            self.db.update_agent(
                agent_id, name, phone, email, license_number, commission_rate
            )
            self.load_agents()

            # Update comboboxes in other tabs
            self.app.property_tab.update_agent_combo()
            self.app.inquiry_tab.update_agent_combo()

            messagebox.showinfo("Success", "Agent updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_agent(self):
        """Delete an agent from the database"""
        selected_item = self.agent_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an agent to delete")
            return

        agent_id = self.agent_tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this agent? This action cannot be undone.",
        )
        if not confirm:
            return

        try:
            self.db.delete_agent(agent_id)
            self.clear_fields()
            self.load_agents()

            # Update comboboxes in other tabs
            self.app.property_tab.update_agent_combo()
            self.app.inquiry_tab.update_agent_combo()

            # Refresh other tabs
            self.app.property_tab.load_properties()
            self.app.inquiry_tab.load_inquiries()

            messagebox.showinfo("Success", "Agent deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_agents(self):
        """Load all agents into the treeview"""
        # Clear existing data
        for i in self.agent_tree.get_children():
            self.agent_tree.delete(i)

        # Load data from database
        agents = self.db.get_agents()

        for row in agents:
            # Format commission rate
            commission_formatted = (
                f"{float(row[6]):.1f}%" if row[6] is not None else "0.0%"
            )

            # Add to treeview
            self.agent_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2] or "",
                    row[3] or "",
                    row[4] or "",
                    row[5],
                    commission_formatted,
                ),
            )

    def search_agents(self):
        """Search agents by name, email, or license number"""
        search_term = self.agent_search_var.get()
        if not search_term:
            self.load_agents()
            return

        # Clear existing data
        for i in self.agent_tree.get_children():
            self.agent_tree.delete(i)

        # Search agents
        agents = self.db.search_agents(search_term)

        for row in agents:
            # Format commission rate
            commission_formatted = (
                f"{float(row[6]):.1f}%" if row[6] is not None else "0.0%"
            )

            # Add to treeview
            self.agent_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2] or "",
                    row[3] or "",
                    row[4] or "",
                    row[5],
                    commission_formatted,
                ),
            )

    def agent_selected(self, event):
        """Handle agent selection in the treeview"""
        selected_item = self.agent_tree.selection()
        if selected_item:
            # Get the agent ID
            agent_id = self.agent_tree.item(selected_item, "values")[0]

            # Get agent details from database
            agent_data = self.db.get_agent(agent_id)
            if agent_data:
                # Clear current fields
                self.clear_fields()

                # Populate fields with selected agent data
                self.agent_name_var.set(agent_data[1])
                self.agent_phone_var.set(agent_data[2] or "")
                self.agent_email_var.set(agent_data[3] or "")
                self.agent_license_var.set(agent_data[4] or "")
                self.agent_commission_var.set(agent_data[6] or 0)

    def clear_fields(self):
        """Clear all input fields"""
        self.agent_name_var.set("")
        self.agent_phone_var.set("")
        self.agent_email_var.set("")
        self.agent_license_var.set("")
        self.agent_commission_var.set("")
