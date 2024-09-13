# PostgreSQL Data Management App

This project provides an interface for managing and visualizing data stored in a PostgreSQL database. It uses Python for backend operations and Shiny for the user interface.

## Features

- **Data Visualization**: Real-time data visualization using a Shiny dashboard.
- **CRUD Operations**: Supports Create, Read, Update, and Delete operations on data stored in PostgreSQL.
- **Data Export**: Users can export the displayed data to a CSV file.

## Prerequisites

- Python 3.8+
- PostgreSQL
- Shiny for Python

## Installation

### Step 1: Install PostgreSQL

1. [Download and install PostgreSQL](https://www.postgresql.org/download/).
2. Ensure that PostgreSQL is running on your system.

### Step 2: Set Up Python Environment

1. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install psycopg2 pandas shiny

### Step 3: Configure Database Connection
Edit the Python script to include your PostgreSQL database credentials:
- Host
- Database name
- User
- Password

### Step 4:  Launch the Shiny App
   ```bash
   python path/to/your_script.py
   ```

## Usage
- Once the Shiny app is running, navigate to the provided URL (typically http://localhost:8080/).
- Use the app's interface to view, add, update, or delete data.
- Export the table data to a CSV file if needed using the provided download button.