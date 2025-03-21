import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_file):
        """Initialize database connection and create tables if they don't exist"""
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create database tables if they don't exist"""
        # Create Property table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                property_type TEXT NOT NULL,
                bedrooms INTEGER,
                bathrooms REAL,
                price REAL,
                listing_date TEXT,
                status TEXT,
                agent_id INTEGER,
                description TEXT
            )
            """
        )

        # Create Agents table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                license_number TEXT,
                join_date TEXT,
                commission_rate REAL
            )
            """
        )

        # Create Inquiries table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                contact_info TEXT,
                property_id INTEGER,
                inquiry_date TEXT,
                status TEXT,
                notes TEXT,
                agent_id INTEGER
            )
            """
        )

        # Create Marketing table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS marketing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                marketing_type TEXT NOT NULL,
                bedrooms INTEGER,
                bathrooms REAL,
                price REAL,
                listing_date TEXT,
                status TEXT,
                agent_id INTEGER,
                description TEXT
            )
            """
        )

        self.conn.commit()

    # Property-related methods
    def add_property(self, address, property_type, bedrooms, bathrooms, price, status, agent_id, description):
        """Add a new property to the database"""
        listing_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """
            INSERT INTO properties (address, property_type, bedrooms, bathrooms, price, listing_date, status, agent_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (address, property_type, bedrooms, bathrooms, price, listing_date, status, agent_id, description),
        )
        self.conn.commit()

    def update_property(self, property_id, address, property_type, bedrooms, bathrooms, price, status, agent_id, description):
        """Update an existing property in the database"""
        self.cursor.execute(
            """
            UPDATE properties
            SET address = ?, property_type = ?, bedrooms = ?, bathrooms = ?, price = ?, status = ?, agent_id = ?, description = ?
            WHERE id = ?
            """,
            (address, property_type, bedrooms, bathrooms, price, status, agent_id, description, property_id),
        )
        self.conn.commit()

    def delete_property(self, property_id):
        """Delete a property and its associated inquiries from the database"""
        self.cursor.execute("DELETE FROM inquiries WHERE property_id = ?", (property_id,))
        self.cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        self.conn.commit()

    def get_properties(self):
        """Get all properties with agent names"""
        self.cursor.execute(
            """
            SELECT p.id, p.address, p.property_type, p.bedrooms, p.bathrooms, p.price, p.status, a.name
            FROM properties p
            LEFT JOIN agents a ON p.agent_id = a.id
            ORDER BY p.id DESC
            """
        )
        return self.cursor.fetchall()

    def get_property(self, property_id):
        """Get a single property by ID"""
        self.cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
        return self.cursor.fetchone()

    def search_properties(self, search_term):
        """Search properties by address or property type"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            """
            SELECT p.id, p.address, p.property_type, p.bedrooms, p.bathrooms, p.price, p.status, a.name
            FROM properties p
            LEFT JOIN agents a ON p.agent_id = a.id
            WHERE p.address LIKE ? OR p.property_type LIKE ?
            ORDER BY p.id DESC
            """,
            (search_pattern, search_pattern),
        )
        return self.cursor.fetchall()

    def get_property_combo_data(self):
        """Get property data for combobox (ID - Address)"""
        self.cursor.execute("SELECT id, address FROM properties ORDER BY address")
        return self.cursor.fetchall()

    # Agent-related methods
    def add_agent(self, name, phone, email, license_number, commission_rate):
        """Add a new agent to the database"""
        join_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """
            INSERT INTO agents (name, phone, email, license_number, join_date, commission_rate)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, phone, email, license_number, join_date, commission_rate),
        )
        self.conn.commit()

    def update_agent(self, agent_id, name, phone, email, license_number, commission_rate):
        """Update an existing agent in the database"""
        self.cursor.execute(
            """
            UPDATE agents
            SET name = ?, phone = ?, email = ?, license_number = ?, commission_rate = ?
            WHERE id = ?
            """,
            (name, phone, email, license_number, commission_rate, agent_id),
        )
        self.conn.commit()

    def delete_agent(self, agent_id):
        """Delete an agent from the database"""
        self.cursor.execute("UPDATE properties SET agent_id = NULL WHERE agent_id = ?", (agent_id,))
        self.cursor.execute("UPDATE inquiries SET agent_id = NULL WHERE agent_id = ?", (agent_id,))
        self.cursor.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
        self.conn.commit()

    def get_agents(self):
        """Get all agents"""
        self.cursor.execute("SELECT * FROM agents ORDER BY name")
        return self.cursor.fetchall()

    def get_agent(self, agent_id):
        """Get a single agent by ID"""
        self.cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
        return self.cursor.fetchone()

    def search_agents(self, search_term):
        """Search agents by name, email, or license number"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            """
            SELECT * FROM agents
            WHERE name LIKE ? OR email LIKE ? OR license_number LIKE ?
            ORDER BY name
            """,
            (search_pattern, search_pattern, search_pattern),
        )
        return self.cursor.fetchall()

    def get_agent_combo_data(self):
        """Get agent data for combobox (ID - Name)"""
        self.cursor.execute("SELECT id, name FROM agents ORDER BY name")
        return self.cursor.fetchall()

    # Inquiry-related methods
    def add_inquiry(self, client_name, contact_info, property_id, status, notes, agent_id):
        """Add a new inquiry to the database"""
        inquiry_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """
            INSERT INTO inquiries (client_name, contact_info, property_id, inquiry_date, status, notes, agent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (client_name, contact_info, property_id, inquiry_date, status, notes, agent_id),
        )
        self.conn.commit()

    def update_inquiry(self, inquiry_id, client_name, contact_info, property_id, status, notes, agent_id):
        """Update an existing inquiry in the database"""
        self.cursor.execute(
            """
            UPDATE inquiries
            SET client_name = ?, contact_info = ?, property_id = ?, status = ?, notes = ?, agent_id = ?
            WHERE id = ?
            """,
            (client_name, contact_info, property_id, status, notes, agent_id, inquiry_id),
        )
        self.conn.commit()

    def delete_inquiry(self, inquiry_id):
        """Delete an inquiry from the database"""
        self.cursor.execute("DELETE FROM inquiries WHERE id = ?", (inquiry_id,))
        self.conn.commit()

    def get_inquiries(self):
        """Get all inquiries with property and agent info"""
        self.cursor.execute(
            """
            SELECT i.id, i.client_name, p.address, i.inquiry_date, i.status, a.name
            FROM inquiries i
            LEFT JOIN properties p ON i.property_id = p.id
            LEFT JOIN agents a ON i.agent_id = a.id
            ORDER BY i.inquiry_date DESC
            """
        )
        return self.cursor.fetchall()

    def get_inquiry(self, inquiry_id):
        """Get a single inquiry by ID"""
        self.cursor.execute("SELECT * FROM inquiries WHERE id = ?", (inquiry_id,))
        return self.cursor.fetchone()

    def search_inquiries(self, search_term):
        """Search inquiries by client name"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            """
            SELECT i.id, i.client_name, p.address, i.inquiry_date, i.status, a.name
            FROM inquiries i
            LEFT JOIN properties p ON i.property_id = p.id
            LEFT JOIN agents a ON i.agent_id = a.id
            WHERE i.client_name LIKE ?
            ORDER BY i.inquiry_date DESC
            """,
            (search_pattern,),
        )
        return self.cursor.fetchall()

    def filter_inquiries_by_status(self, status):
        """Filter inquiries by status"""
        self.cursor.execute(
            """
            SELECT i.id, i.client_name, p.address, i.inquiry_date, i.status, a.name
            FROM inquiries i
            LEFT JOIN properties p ON i.property_id = p.id
            LEFT JOIN agents a ON i.agent_id = a.id
            WHERE i.status = ?
            ORDER BY i.inquiry_date DESC
            """,
            (status,),
        )
        return self.cursor.fetchall()

    # Marketing-related methods
    def add_marketing(self, address, marketing_type, bedrooms, bathrooms, price, status, agent_id, description):
        """Add a new marketing entry to the database"""
        listing_date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """
            INSERT INTO marketing (address, marketing_type, bedrooms, bathrooms, price, listing_date, status, agent_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (address, marketing_type, bedrooms, bathrooms, price, listing_date, status, agent_id, description),
        )
        self.conn.commit()

    def update_marketing(self, marketing_id, address, marketing_type, bedrooms, bathrooms, price, status, agent_id, description):
        """Update an existing marketing entry in the database"""
        self.cursor.execute(
            """
            UPDATE marketing
            SET address = ?, marketing_type = ?, bedrooms = ?, bathrooms = ?, price = ?, status = ?, agent_id = ?, description = ?
            WHERE id = ?
            """,
            (address, marketing_type, bedrooms, bathrooms, price, status, agent_id, description, marketing_id),
        )
        self.conn.commit()

    def delete_marketing(self, marketing_id):
        """Delete a marketing entry from the database"""
        self.cursor.execute("DELETE FROM marketing WHERE id = ?", (marketing_id,))
        self.conn.commit()

    def get_marketing_entries(self):
        """Get all marketing entries with agent names"""
        self.cursor.execute(
            """
            SELECT m.id, m.address, m.marketing_type, m.bedrooms, m.bathrooms, m.price, m.status, a.name
            FROM marketing m
            LEFT JOIN agents a ON m.agent_id = a.id
            ORDER BY m.id DESC
            """
        )
        return self.cursor.fetchall()

    def search_marketing_entries(self, search_term):
        """Search marketing entries by address or marketing type"""
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            """
            SELECT m.id, m.address, m.marketing_type, m.bedrooms, m.bathrooms, m.price, m.status, a.name
            FROM marketing m
            LEFT JOIN agents a ON m.agent_id = a.id
            WHERE m.address LIKE ? OR m.marketing_type LIKE ?
            ORDER BY m.id DESC
            """,
            (search_pattern, search_pattern),
        )
        return self.cursor.fetchall()

    def get_marketing(self, marketing_id):
        """Get a single marketing entry by ID"""
        self.cursor.execute("SELECT * FROM marketing WHERE id = ?", (marketing_id,))
        return self.cursor.fetchone()