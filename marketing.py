import tkinter as tk
from tkinter import ttk, messagebox

class MarketingTab:
    def __init__(self, parent, database, app):
        """Initialize the Marketing tab"""
        self.parent = parent
        self.db = database
        self.app = app

        # Variables for entry fields
        self.address_var = tk.StringVar()
        self.property_type_var = tk.StringVar()
        self.bedrooms_var = tk.StringVar()
        self.bathrooms_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.agent_id_var = tk.StringVar()
        self.property_search_var = tk.StringVar()

        # Create the tab UI
        self.create_tab()

    def create_tab(self):
        """Create the marketing tab UI"""
        marketing_frame = ttk.Frame(self.parent)
        self.parent.add(marketing_frame, text="Marketing")

        # Left frame for property entry
        left_frame = ttk.Frame(marketing_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for property listing
        right_frame = ttk.Frame(marketing_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Property input fields
        ttk.Label(
            left_frame, text="Marketing", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(left_frame, text="Address:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(left_frame, textvariable=self.address_var, width=40).grid(
            row=1, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Property Type:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        property_types = [
            "Apartment",
            "House",
            "Condo",
            "Townhouse",
            "Land",
            "Commercial",
        ]
        ttk.Combobox(
            left_frame,
            textvariable=self.property_type_var,
            values=property_types,
            width=15,
        ).grid(row=2, column=1, pady=5, sticky=tk.W)

        ttk.Label(left_frame, text="Bedrooms:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        ttk.Spinbox(
            left_frame, from_=0, to=10, textvariable=self.bedrooms_var, width=5
        ).grid(row=3, column=1, pady=5, sticky=tk.W)

        ttk.Label(left_frame, text="Bathrooms:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        ttk.Spinbox(
            left_frame,
            from_=0,
            to=10,
            increment=0.5,
            textvariable=self.bathrooms_var,
            width=5,
        ).grid(row=4, column=1, pady=5, sticky=tk.W)

        ttk.Label(left_frame, text="Price ($):").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(left_frame, textvariable=self.price_var, width=15).grid(
            row=5, column=1, pady=5, sticky=tk.W
        )

        ttk.Label(left_frame, text="Status:").grid(row=6, column=0, sticky=tk.W, pady=5)
        status_types = ["Available", "Pending", "Sold", "Off Market"]
        ttk.Combobox(
            left_frame, textvariable=self.status_var, values=status_types, width=15
        ).grid(row=6, column=1, pady=5, sticky=tk.W)

        ttk.Label(left_frame, text="Agent:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.agent_combo = ttk.Combobox(
            left_frame, textvariable=self.agent_id_var, width=25
        )
        self.agent_combo.grid(row=7, column=1, pady=5, sticky=tk.W)
        self.update_agent_combo()

        ttk.Label(left_frame, text="Description:").grid(
            row=8, column=0, sticky=tk.W, pady=5
        )
        self.description_text = tk.Text(left_frame, width=40, height=5)
        self.description_text.grid(row=8, column=1, pady=5, sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Property", command=self.add_property).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="Update Property", command=self.update_property
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Delete Property", command=self.delete_property
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(
            side=tk.LEFT, padx=5
        )

        # Property listing
        ttk.Label(
            right_frame, text="Property Listings", font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Search frame
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(search_frame, textvariable=self.property_search_var, width=20).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Search", command=self.search_properties).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Show All", command=self.load_properties).pack(
            side=tk.LEFT, padx=5
        )

        # Treeview for property listing
        columns = ("id", "address", "type", "beds", "baths", "price", "status", "agent")
        self.property_tree = ttk.Treeview(
            right_frame, columns=columns, show="headings", height=15
        )

        # Define headings
        self.property_tree.heading("id", text="ID")
        self.property_tree.heading("address", text="Address")
        self.property_tree.heading("type", text="Type")
        self.property_tree.heading("beds", text="Beds")
        self.property_tree.heading("baths", text="Baths")
        self.property_tree.heading("price", text="Price ($)")
        self.property_tree.heading("status", text="Status")
        self.property_tree.heading("agent", text="Agent")

        # Define columns
        self.property_tree.column("id", width=40)
        self.property_tree.column("address", width=200)
        self.property_tree.column("type", width=80)
        self.property_tree.column("beds", width=50)
        self.property_tree.column("baths", width=50)
        self.property_tree.column("price", width=100)
        self.property_tree.column("status", width=80)
        self.property_tree.column("agent", width=150)

        # Add scrollbar
        property_scrollbar = ttk.Scrollbar(
            right_frame, orient=tk.VERTICAL, command=self.property_tree.yview
        )
        self.property_tree.configure(yscrollcommand=property_scrollbar.set)

        # Pack tree and scrollbar
        self.property_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        property_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind select event
        self.property_tree.bind("<<TreeviewSelect>>", self.property_selected)

        # Load data
        self.load_properties()

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

    def add_property(self):
        """Add a new property to the database"""
        address = self.address_var.get()
        property_type = self.property_type_var.get()
        bedrooms = self.bedrooms_var.get()
        bathrooms = self.bathrooms_var.get()
        price = self.price_var.get()
        status = self.status_var.get()
        agent_id = self.get_id_from_combobox(self.agent_id_var.get())
        description = self.description_text.get("1.0", tk.END).strip()

        if not address or not property_type:
            messagebox.showerror(
                "Error", "Address and Property Type are required fields"
            )
            return

        try:
            bedrooms = int(bedrooms) if bedrooms else 0
            bathrooms = float(bathrooms) if bathrooms else 0
            price = float(price) if price else 0

            self.db.add_property(
                address,
                property_type,
                bedrooms,
                bathrooms,
                price,
                status,
                agent_id,
                description,
            )
            self.clear_fields()
            self.load_properties()
            self.app.inquiry_tab.update_property_combo()

            messagebox.showinfo("Success", "Property added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_property(self):
        """Update an existing property in the database"""
        selected_item = self.property_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a property to update")
            return

        property_id = self.property_tree.item(selected_item, "values")[0]
        address = self.address_var.get()
        property_type = self.property_type_var.get()
        bedrooms = self.bedrooms_var.get()
        bathrooms = self.bathrooms_var.get()
        price = self.price_var.get()
        status = self.status_var.get()
        agent_id = self.get_id_from_combobox(self.agent_id_var.get())
        description = self.description_text.get("1.0", tk.END).strip()

        if not address or not property_type:
            messagebox.showerror(
                "Error", "Address and Property Type are required fields"
            )
            return

        try:
            bedrooms = int(bedrooms) if bedrooms else 0
            bathrooms = float(bathrooms) if bathrooms else 0
            price = float(price) if price else 0

            self.db.update_property(
                property_id,
                address,
                property_type,
                bedrooms,
                bathrooms,
                price,
                status,
                agent_id,
                description,
            )
            self.load_properties()
            self.app.inquiry_tab.update_property_combo()

            messagebox.showinfo("Success", "Property updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_property(self):
        """Delete a property and its associated inquiries from the database"""
        selected_item = self.property_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a property to delete")
            return

        property_id = self.property_tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this property? This action cannot be undone.",
        )
        if not confirm:
            return

        try:
            self.db.delete_property(property_id)
            self.clear_fields()
            self.load_properties()
            self.app.inquiry_tab.load_inquiries()
            self.app.inquiry_tab.update_property_combo()

            messagebox.showinfo("Success", "Property deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_properties(self):
        """Load all properties into the treeview"""
        # Clear existing data
        for i in self.property_tree.get_children():
            self.property_tree.delete(i)

        # Load data from database
        properties = self.db.get_properties()

        for row in properties:
            # Format price as INR currency
            price_in_lakhs = row[5] / 100000
            if price_in_lakhs >= 100:
                # Display in crores if >= 1 crore
                price_in_crores = price_in_lakhs / 100
                price_formatted = f"₹{price_in_crores:.2f} Cr"
            else:
                # Display in lakhs
                price_formatted = f"₹{price_in_lakhs:.2f} L"

            # Format bedrooms and bathrooms
            beds = int(row[3]) if row[3] else 0
            baths = float(row[4]) if row[4] else 0
            baths_formatted = int(baths) if baths.is_integer() else baths

            # Add to treeview with formatted values
            self.property_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    beds,
                    baths_formatted,
                    price_formatted,
                    row[6],
                    row[7] or "None",
                ),
            )

    def search_properties(self):
        """Search properties by address or property type"""
        search_term = self.property_search_var.get()
        if not search_term:
            self.load_properties()
            return

        # Clear existing data
        for i in self.property_tree.get_children():
            self.property_tree.delete(i)

        # Search properties
        properties = self.db.search_properties(search_term)

        for row in properties:
            # Format price as INR currency
            price_in_lakhs = row[5] / 100000
            if price_in_lakhs >= 100:
                # Display in crores if >= 1 crore
                price_in_crores = price_in_lakhs / 100
                price_formatted = f"₹{price_in_crores:.2f} Cr"
            else:
                # Display in lakhs
                price_formatted = f"₹{price_in_lakhs:.2f} L"

            # Format bedrooms and bathrooms
            beds = int(row[3]) if row[3] else 0
            baths = float(row[4]) if row[4] else 0
            baths_formatted = int(baths) if baths.is_integer() else baths

            # Add to treeview with formatted values
            self.property_tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    beds,
                    baths_formatted,
                    price_formatted,
                    row[6],
                    row[7] or "None",
                ),
            )

    def property_selected(self, event):
        """Handle property selection in the treeview"""
        selected_item = self.property_tree.selection()
        if selected_item:
            # Get the property ID
            property_id = self.property_tree.item(selected_item, "values")[0]

            # Get property details from database
            property_data = self.db.get_property(property_id)
            if property_data:
                # Clear current fields
                self.clear_fields()

                # Populate fields with selected property data
                self.address_var.set(property_data[1])
                self.property_type_var.set(property_data[2])
                self.bedrooms_var.set(property_data[3])
                self.bathrooms_var.set(property_data[4])
                self.price_var.set(property_data[5])
                self.status_var.set(property_data[7])

                # Set agent if exists
                if property_data[8]:
                    # Find agent in combobox values
                    agent_values = self.agent_combo["values"]
                    for agent_value in agent_values:
                        if agent_value.startswith(f"{property_data[8]} - "):
                            self.agent_id_var.set(agent_value)
                            break

                # Set description
                self.description_text.delete("1.0", tk.END)
                if property_data[9]:
                    self.description_text.insert("1.0", property_data[9])

    def clear_fields(self):
        """Clear all input fields"""
        self.address_var.set("")
        self.property_type_var.set("")
        self.bedrooms_var.set("")
        self.bathrooms_var.set("")
        self.price_var.set("")
        self.status_var.set("")
        self.agent_id_var.set("")
        self.description_text.delete("1.0", tk.END)