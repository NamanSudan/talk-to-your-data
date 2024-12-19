import os
import sqlite3
import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the database directory exists
DB_PATH = Path('data.db')

def get_db_connection():
    """Create a database connection"""
    try:
        conn = sqlite3.connect('data.db')
        # Enable foreign keys
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        raise

def init_database():
    """Initialize the database with sample tables and data"""
    try:
        conn = get_db_connection()
        logging.info("Database connection established successfully")
        # Create tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount DECIMAL(10,2),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Insert sample data if tables are empty
        if not pd.read_sql_query("SELECT * FROM users", conn).shape[0]:
            sample_users = [
                (1, "John Doe", "john@example.com"),
                (2, "Jane Smith", "jane@example.com"),
                (3, "Bob Wilson", "bob@example.com")
            ]
            conn.executemany(
                "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                sample_users
            )
        
        if not pd.read_sql_query("SELECT * FROM orders", conn).shape[0]:
            sample_orders = [
                (1, 1, 100.50),
                (2, 1, 200.75),
                (3, 2, 150.25),
                (4, 3, 300.00)
            ]
            conn.executemany(
                "INSERT INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
                sample_orders
            )
        
        conn.commit()
        logging.info("Database initialized successfully")
    except sqlite3.Error as e:
        logging.exception(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed")