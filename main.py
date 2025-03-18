import tkinter as tk
from database import Database
from app import RealEstateApp
from seed_data import seed_database
import os


def main():
    # Check if database exists, if not, create and seed it
    if not os.path.exists("real_estate.db"):
        print("Database not found. Creating and seeding with sample data...")
        seed_database()
    else:
        # Check if database is empty
        db = Database("real_estate.db")
        db.cursor.execute("SELECT COUNT(*) FROM properties")
        property_count = db.cursor.fetchone()[0]

        db.cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = db.cursor.fetchone()[0]

        db.cursor.execute("SELECT COUNT(*) FROM inquiries")
        inquiry_count = db.cursor.fetchone()[0]

        if property_count == 0 and agent_count == 0 and inquiry_count == 0:
            print("Database is empty. Seeding with sample data...")
            db.close()
            seed_database()
        else:
            db.close()

    # Initialize the root window
    root = tk.Tk()

    # Create the database connection
    db = Database("real_estate.db")

    # Initialize the application with the root window and database
    app = RealEstateApp(root, db)

    # Run the application
    root.mainloop()

    # Close the database connection when the application closes
    db.close()


if __name__ == "__main__":
    main()
