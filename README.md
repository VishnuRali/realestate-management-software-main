# Indian Real Estate Management System

A comprehensive real estate management application built with Python and Tkinter. This application is designed for Indian real estate agencies to manage properties, agents, and client inquiries in one place, with support for Indian currency (INR) and location formats.

## Features

- **Property Management**: Add, edit, and delete property listings with details like address, type, price (in INR), and status.
- **Agent Registration**: Manage real estate agents including their contact information and commission rates.
- **Client Inquiry Tracking**: Track client inquiries, viewings, and the status of their property interests.
- **Sample Data**: Comes with pre-seeded Indian real estate data for immediate testing and use.

## Requirements

- Python 3.6+ 
- Tkinter (usually comes with Python)
- SQLite3 (included in Python standard library)

## Installation and Setup

### Setting Up a Virtual Environment (Recommended)

Using a virtual environment is recommended to avoid conflicts with other Python projects:

#### For Windows:
```bash
# Navigate to your project directory
cd path/to/real-estate-system

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install required packages (if any additional ones were needed)
pip install -r requirements.txt  # If you have a requirements.txt file
```

#### For macOS/Linux:
```bash
# Navigate to your project directory
cd path/to/real-estate-system

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages (if any additional ones were needed)
pip install -r requirements.txt  # If you have a requirements.txt file
```

### Running the Application

With your virtual environment activated:

```bash
python main.py
```

### Deactivating the Virtual Environment

When you're done working with the application:

```bash
deactivate
```

## Building Executables

### Creating a Windows Executable (.exe)

To build a Windows executable, you need to be on a Windows system or use a Windows virtual machine:

```bash
# Make sure PyInstaller is installed
pip install pyinstaller

# Create the executable
pyinstaller --onefile --windowed --name="Indian_Real_Estate_Manager" main.py
```

The executable will be available in the `dist` directory.

### Creating a macOS Application (.app)

To build a macOS application, you need to be on a macOS system:

```bash
# Make sure PyInstaller is installed
pip install pyinstaller

# Create the application
pyinstaller --windowed --name="Indian_Real_Estate_Manager" main.py
```

The application will be available in the `dist` directory.

## Application Structure

- `main.py`: Main entry point for the application
- `app.py`: Core application class that sets up the UI
- `database.py`: Database connection and operations
- `property.py`: Property management tab implementation
- `agent.py`: Agent registration tab implementation
- `inquiry.py`: Client inquiry tracking tab implementation
- `seed_data.py`: Script for populating the database with sample Indian real estate data

## Database

The application uses SQLite to store data in a file named `real_estate.db`. This database is automatically created and populated with sample data when the application is run for the first time.

## Sample Data

The application comes with pre-seeded data including:

- **Properties**: Apartments, villas, houses, and commercial spaces in cities like Mumbai, Bangalore, Delhi, and more
- **Pricing**: All prices are in Indian Rupees (₹), displayed in lakhs and crores
- **Agents**: Indian real estate agents with their contact details
- **Inquiries**: Sample client inquiries in various stages of the property buying process

## Usage Guide

### Property Management

1. Fill in the property details in the left panel
2. Click "Add Property" to add a new listing
3. Select a property in the right panel to edit or delete it
4. Use the search bar to find properties

### Agent Registration

1. Enter agent details in the left panel
2. Click "Add Agent" to register a new agent
3. Select an agent in the right panel to edit or delete
4. Use the search bar to find agents by name, email, or license number

### Client Inquiry Tracking

1. Enter client and inquiry details in the left panel
2. Select a property and assigned agent from dropdown lists
3. Add notes about the client inquiry
4. Use the status dropdown to track the progress of inquiries
5. Filter inquiries by status using the filter dropdown

## Troubleshooting

### Tkinter Not Found
If you encounter an error about missing Tkinter:

#### On macOS:
```bash
brew install python-tk
```

#### On Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

### Database Issues
If the database becomes corrupted, you can reset it by:
1. Close the application
2. Delete the `real_estate.db` file
3. Restart the application (a new database will be created with sample data)

## License

This project is provided for educational purposes.

## Support

For any issues or questions, please contact the developer.
