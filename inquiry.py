import tkinter as tk
from tkinter import ttk, messagebox


class InquiryTab:
    def __init__(self, parent, database, app):
        """Initialize the Client Inquiry Tracking tab"""
        self.parent = parent
        self.db = database
        self.app = app

        # Variables for entry fields
        self.client_name_var = tk.StringVar()
        self.contact_info_var = tk.StringVar()
        self.property_id_var = tk.StringVar()
        self.inquiry_agent_id_var = tk.StringVar()
        self.inquiry_status_var = tk.StringVar()
        self.inquiry_search_var = tk.StringVar()
        self.inquiry_filter_var = tk.StringVar()
        self.inquiry_filter_var.set("All")

        # Create the tab UI
        self.create_tab()

    def create_tab(self):
        """Create the Client Inquiry Tracking tab UI"""
        inquiry_frame = ttk.Frame(self.parent)
        self.parent.add(inquiry_frame, text="Client Inquiry Tracking")

        # Left frame for inquiry entry
        left_frame = ttk.Frame(inquiry_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for inquiry listing
        right_frame = ttk.Frame(inquiry_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Inquiry input fields
        ttk.Label(
            left_frame, text="Client Inquiry Tracking", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(left_frame, text="Client Name:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(left_frame, textvariable=self.client_name_var, width=30).grid(
            row=1, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Contact Info:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(left_frame, textvariable=self.contact_info_var, width=30).grid(
            row=2, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Property:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.property_combo = ttk.Combobox(
            left_frame, textvariable=self.property_id_var, width=30
        )
        self.property_combo.grid(row=3, column=1, pady=5, sticky=tk.W)
        self.update_property_combo()

        ttk.Label(left_frame, text="Assigned Agent:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.agent_combo = ttk.Combobox(
            left_frame, textvariable=self.inquiry_agent_id_var, width=25
        )
        self.agent_combo.grid(row=4, column=1, pady=5, sticky=tk.W)
        self.update_agent_combo()

        ttk.Label(left_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, pady=5)
        status_types = [
            "New",
            "Contacted",
            "Viewing Scheduled",
            "Offer Made",
            "Closed",
            "Cancelled",
        ]
        ttk.Combobox(
            left_frame,
            textvariable=self.inquiry_status_var,
            values=status_types,
            width=15,
        ).grid(row=5, column=1, pady=5, sticky=tk.W)

        ttk.Label(left_frame, text="Notes:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(left_frame, width=40, height=5)
        self.notes_text.grid(row=6, column=1, pady=5, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Inquiry", command=self.add_inquiry).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="Update Inquiry", command=self.update_inquiry
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Delete Inquiry", command=self.delete_inquiry
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(
            side=tk.LEFT, padx=5
        )

        # Inquiry listing
        ttk.Label(
            right_frame, text="Client Inquiries", font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Search frame
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(search_frame, textvariable=self.inquiry_search_var, width=20).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Search", command=self.search_inquiries).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Show All", command=self.load_inquiries).pack(
            side=tk.LEFT, padx=5
        )

        # Filter by status
        filter_frame = ttk.Frame(right_frame)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=5)
        status_filter = ["All"] + status_types
        ttk.Combobox(
            filter_frame,
            textvariable=self.inquiry_filter_var,
            values=status_filter,
            width=15,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            filter_frame, text="Apply Filter", command=self.filter_inquiries
        ).pack(side=tk.LEFT, padx=5)

        # Treeview for inquiry listing
        columns = ("id", "client", "property", "date", "status", "agent")
        self.inquiry_tree = ttk.Treeview(
            right_frame, columns=columns, show="headings", height=15
        )

        # Define headings
        self.inquiry_tree.heading("id", text="ID")
        self.inquiry_tree.heading("client", text="Client")
        self.inquiry_tree.heading("property", text="Property")
        self.inquiry_tree.heading("date", text="Inquiry Date")
        self.inquiry_tree.heading("status", text="Status")
        self.inquiry_tree.heading("agent", text="Agent")

        # Define columns
        self.inquiry_tree.column("id", width=40)
        self.inquiry_tree.column("client", width=150)
        self.inquiry_tree.column("property", width=200)
        self.inquiry_tree.column("date", width=100)
        self.inquiry_tree.column("status", width=120)
        self.inquiry_tree.column("agent", width=150)

        # Add scrollbar
        inquiry_scrollbar = ttk.Scrollbar(
            right_frame, orient=tk.VERTICAL, command=self.inquiry_tree.yview
        )
        self.inquiry_tree.configure(yscrollcommand=inquiry_scrollbar.set)

        # Pack tree and scrollbar
        self.inquiry_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inquiry_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind select event
        self.inquiry_tree.bind("<<TreeviewSelect>>", self.inquiry_selected)

        # Load data
        self.load_inquiries()

    def update_property_combo(self):
        """Update the property combobox with current data"""
        self.property_combo.set("")
        properties = self.db.get_property_combo_data()
        property_list = [f"{prop[0]} - {prop[1]}" for prop in properties]
        self.property_combo["values"] = property_list

    def update_agent_combo(self):
        """Update the agent combobox with current data"""
        self.agent_combo.set("")
        agents = self.db.get_agent_combo_data()
        agent_list = [f"{agent[0]} - {agent[1]}" for agent in agents]
        self.agent_combo["values"] = agent_list

    def get_id_from_combobox(self, combo_value):
        """Extract ID from combobox value (format: "ID - Value")"""
        if not combo_value:
            return None

        try:
            return int(combo_value.split(" - ")[0])
        except (ValueError, IndexError):
            return None

    def add_inquiry(self):
        """Add a new inquiry to the database"""
        client_name = self.client_name_var.get()
        contact_info = self.contact_info_var.get()
        property_id = self.get_id_from_combobox(self.property_id_var.get())
        agent_id = self.get_id_from_combobox(self.inquiry_agent_id_var.get())
        status = self.inquiry_status_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not client_name:
            messagebox.showerror("Error", "Client Name is a required field")
            return

        try:
            self.db.add_inquiry(
                client_name, contact_info, property_id, status, notes, agent_id
            )
            self.clear_fields()
            self.load_inquiries()

            messagebox.showinfo("Success", "Inquiry added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_inquiry(self):
        """Update an existing inquiry in the database"""
        selected_item = self.inquiry_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an inquiry to update")
            return

        inquiry_id = self.inquiry_tree.item(selected_item, "values")[0]
        client_name = self.client_name_var.get()
        contact_info = self.contact_info_var.get()
        property_id = self.get_id_from_combobox(self.property_id_var.get())
        agent_id = self.get_id_from_combobox(self.inquiry_agent_id_var.get())
        status = self.inquiry_status_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not client_name:
            messagebox.showerror("Error", "Client Name is a required field")
            return

        try:
            self.db.update_inquiry(
                inquiry_id,
                client_name,
                contact_info,
                property_id,
                status,
                notes,
                agent_id,
            )
            self.load_inquiries()

            messagebox.showinfo("Success", "Inquiry updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_inquiry(self):
        """Delete an inquiry from the database"""
        selected_item = self.inquiry_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an inquiry to delete")
            return

        inquiry_id = self.inquiry_tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this inquiry? This action cannot be undone.",
        )
        if not confirm:
            return

        try:
            self.db.delete_inquiry(inquiry_id)
            self.clear_fields()
            self.load_inquiries()

            messagebox.showinfo("Success", "Inquiry deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_inquiries(self):
        """Load all inquiries into the treeview"""
        # Clear existing data
        for i in self.inquiry_tree.get_children():
            self.inquiry_tree.delete(i)

        # Load data from database
        inquiries = self.db.get_inquiries()

        for row in inquiries:
            # Add to treeview
            self.inquiry_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2] or "N/A",
                    row[3],
                    row[4] or "New",
                    row[5] or "Unassigned",
                ),
            )

    def search_inquiries(self):
        """Search inquiries by client name"""
        search_term = self.inquiry_search_var.get()
        if not search_term:
            self.load_inquiries()
            return

        # Clear existing data
        for i in self.inquiry_tree.get_children():
            self.inquiry_tree.delete(i)

        # Search inquiries
        inquiries = self.db.search_inquiries(search_term)

        for row in inquiries:
            # Add to treeview
            self.inquiry_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2] or "N/A",
                    row[3],
                    row[4] or "New",
                    row[5] or "Unassigned",
                ),
            )

    def filter_inquiries(self):
        """Filter inquiries by status"""
        status = self.inquiry_filter_var.get()
        if status == "All":
            self.load_inquiries()
            return

        # Clear existing data
        for i in self.inquiry_tree.get_children():
            self.inquiry_tree.delete(i)

        # Filter inquiries
        inquiries = self.db.filter_inquiries_by_status(status)

        for row in inquiries:
            # Add to treeview
            self.inquiry_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2] or "N/A",
                    row[3],
                    row[4] or "New",
                    row[5] or "Unassigned",
                ),
            )

    def inquiry_selected(self, event):
        """Handle inquiry selection in the treeview"""
        selected_item = self.inquiry_tree.selection()
        if selected_item:
            # Get the inquiry ID
            inquiry_id = self.inquiry_tree.item(selected_item, "values")[0]

            # Get inquiry details from database
            inquiry_data = self.db.get_inquiry(inquiry_id)
            if inquiry_data:
                # Clear current fields
                self.clear_fields()

                # Populate fields with selected inquiry data
                self.client_name_var.set(inquiry_data[1])
                self.contact_info_var.set(inquiry_data[2] or "")

                # Set property if exists
                if inquiry_data[3]:
                    # Find property in combobox values
                    property_values = self.property_combo["values"]
                    for property_value in property_values:
                        if property_value.startswith(f"{inquiry_data[3]} - "):
                            self.property_id_var.set(property_value)
                            break

                self.inquiry_status_var.set(inquiry_data[5] or "New")

                # Set agent if exists
                if inquiry_data[7]:
                    # Find agent in combobox values
                    agent_values = self.agent_combo["values"]
                    for agent_value in agent_values:
                        if agent_value.startswith(f"{inquiry_data[7]} - "):
                            self.inquiry_agent_id_var.set(agent_value)
                            break

                # Set notes
                self.notes_text.delete("1.0", tk.END)
                if inquiry_data[6]:
                    self.notes_text.insert("1.0", inquiry_data[6])

    def clear_fields(self):
        """Clear all input fields"""
        self.client_name_var.set("")
        self.contact_info_var.set("")
        self.property_id_var.set("")
        self.inquiry_agent_id_var.set("")
        self.inquiry_status_var.set("")
        self.notes_text.delete("1.0", tk.END)
