import sqlite3
from datetime import datetime, timedelta
import random
import os


def seed_database(db_path="real_estate.db"):
    """Seed the database with sample Indian real estate data"""

    # Check if database already has data
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if there are any existing records
        cursor.execute("SELECT COUNT(*) FROM properties")
        property_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM inquiries")
        inquiry_count = cursor.fetchone()[0]

        conn.close()

        # If there's already data, don't seed
        if property_count > 0 or agent_count > 0 or inquiry_count > 0:
            print("Database already contains data. Skipping seed operation.")
            return

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute(
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

    cursor.execute(
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

    cursor.execute(
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

    conn.commit()

    # Sample data for agents
    agents = [
        (
            "Rajesh Sharma",
            "9876543210",
            "rajesh.sharma@realestate.co.in",
            "RERA12345",
            (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            2.0,
        ),
        (
            "Priya Patel",
            "8765432109",
            "priya.patel@realestate.co.in",
            "RERA23456",
            (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d"),
            1.5,
        ),
        (
            "Amit Kumar",
            "7654321098",
            "amit.kumar@realestate.co.in",
            "RERA34567",
            (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
            2.5,
        ),
        (
            "Sneha Reddy",
            "6543210987",
            "sneha.reddy@realestate.co.in",
            "RERA45678",
            (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
            1.75,
        ),
        (
            "Vikram Singh",
            "9876123450",
            "vikram.singh@realestate.co.in",
            "RERA56789",
            (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
            2.25,
        ),
    ]

    # Insert agents
    for agent in agents:
        cursor.execute(
            """
            INSERT INTO agents (name, phone, email, license_number, join_date, commission_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            agent,
        )

    conn.commit()

    # Get agent IDs for reference
    cursor.execute("SELECT id FROM agents")
    agent_ids = [row[0] for row in cursor.fetchall()]

    # Sample data for properties (Indian cities, localities, and INR prices)
    properties = [
        (
            "A-201, Greenview Apartments, Powai, Mumbai 400076",
            "Apartment",
            3,
            2,
            9500000,
            (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Spacious 3BHK in premium society with swimming pool, gym, and children's play area. Walking distance from Hiranandani Gardens.",
        ),
        (
            "Villa 15, Palm Meadows, Whitefield, Bangalore 560066",
            "Villa",
            4,
            3.5,
            15000000,
            (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Luxurious 4BHK villa with private garden in gated community. Close to ITPL and top international schools.",
        ),
        (
            "C-12, DLF Phase 2, Gurugram 122002",
            "Independent House",
            5,
            4,
            22500000,
            (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "Pending",
            random.choice(agent_ids),
            "Elegant 5BHK independent house with modern amenities. Excellent connectivity to Delhi via NH-8.",
        ),
        (
            "Flat 304, Sunshine Tower, Banjara Hills, Hyderabad 500034",
            "Apartment",
            2,
            2,
            6800000,
            (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Contemporary 2BHK apartment with city views. Well-maintained society with 24/7 security.",
        ),
        (
            "42, Model Town, Ludhiana 141002",
            "Kothi",
            3,
            3,
            7500000,
            (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Traditional Punjab-style kothi with modern interiors. Large terrace and spacious rooms.",
        ),
        (
            "B-15, Aundh, Pune 411007",
            "Row House",
            3,
            2.5,
            11000000,
            (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Beautifully designed row house in premium locality. Close to IT hubs and educational institutions.",
        ),
        (
            "Flat 1203, Sea View Heights, Marine Drive, Mumbai 400020",
            "Apartment",
            1,
            1,
            12000000,
            (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Premium 1BHK with breathtaking sea view. Perfect for investment with high rental potential.",
        ),
        (
            "Shop 12, Connaught Place, New Delhi 110001",
            "Commercial",
            0,
            1,
            35000000,
            datetime.now().strftime("%Y-%m-%d"),
            "Available",
            random.choice(agent_ids),
            "Prime commercial space in Delhi's business hub. Excellent frontage and high footfall area.",
        ),
        (
            "Plot 25, Sector 45, Noida 201301",
            "Land",
            0,
            0,
            8000000,
            (datetime.now() - timedelta(days=75)).strftime("%Y-%m-%d"),
            "Sold",
            random.choice(agent_ids),
            "250 sq. yard plot in developed sector. Rectangular shape with road on two sides.",
        ),
        (
            "D-404, Prestige Shantiniketan, Whitefield, Bangalore 560048",
            "Apartment",
            3,
            2,
            8900000,
            (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
            "Off Market",
            random.choice(agent_ids),
            "Spacious 3BHK in integrated township with excellent amenities. Close to metro station and shopping centers.",
        ),
    ]

    # Insert properties
    for prop in properties:
        cursor.execute(
            """
            INSERT INTO properties (address, property_type, bedrooms, bathrooms, price, listing_date, status, agent_id, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            prop,
        )

    conn.commit()

    # Get property IDs for reference
    cursor.execute("SELECT id FROM properties")
    property_ids = [row[0] for row in cursor.fetchall()]

    # Sample data for inquiries (Indian names and contact info)
    inquiries = [
        (
            "Rahul Verma",
            "rahul.verma@email.com",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
            "New",
            "Looking for property close to his office in Mumbai. Budget 1-1.2 cr.",
            random.choice(agent_ids),
        ),
        (
            "Ananya Gupta",
            "9876543210",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
            "Contacted",
            "Called client to discuss property details. Interested in east-facing apartments only.",
            random.choice(agent_ids),
        ),
        (
            "Suresh Menon",
            "suresh.menon@email.com",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "Viewing Scheduled",
            "Site visit scheduled for Sunday at 11:00 AM. Client coming with family.",
            random.choice(agent_ids),
        ),
        (
            "Pooja Iyer",
            "9876123450",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
            "Offer Made",
            "Client has submitted an offer of ₹83 lakhs. Awaiting seller response.",
            random.choice(agent_ids),
        ),
        (
            "Karan Malhotra",
            "karan.malhotra@email.com",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "New",
            "NRI customer looking for investment property in Bangalore. Prefers new construction.",
            random.choice(agent_ids),
        ),
        (
            "Neha Sharma",
            "9871234560",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "Contacted",
            "Left message. Client is looking for property for her parents. Needs ground floor.",
            random.choice(agent_ids),
        ),
        (
            "Arjun Nair",
            "arjun.nair@email.com",
            random.choice(property_ids),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "New",
            "Interested in gated communities in Whitefield area. Budget up to ₹1.5 cr.",
            random.choice(agent_ids),
        ),
        (
            "Meera Desai",
            "9898765432",
            random.choice(property_ids),
            datetime.now().strftime("%Y-%m-%d"),
            "New",
            "First-time homebuyer looking for 2BHK in Pune. Has pre-approved loan.",
            random.choice(agent_ids),
        ),
    ]

    # Insert inquiries
    for inquiry in inquiries:
        cursor.execute(
            """
            INSERT INTO inquiries (client_name, contact_info, property_id, inquiry_date, status, notes, agent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            inquiry,
        )

    conn.commit()
    conn.close()

    print("Database seeded successfully with Indian real estate sample data.")


if __name__ == "__main__":
    seed_database()
