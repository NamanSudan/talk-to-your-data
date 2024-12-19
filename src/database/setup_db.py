import sqlite3
import pandas as pd

def initialize_database():
    """
    Initialize SQLite database with sample data
    """
    conn = sqlite3.connect('data.db')
    
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
    
    # Insert sample data
    sample_users = [
        (1, "John Doe", "john@example.com"),
        (2, "Jane Smith", "jane@example.com")
    ]
    
    sample_orders = [
        (1, 1, 100.50),
        (2, 1, 200.75),
        (3, 2, 150.25)
    ]
    
    conn.executemany(
        "INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)",
        sample_users
    )
    
    conn.executemany(
        "INSERT OR IGNORE INTO orders (id, user_id, amount) VALUES (?, ?, ?)",
        sample_orders
    )
    
    conn.commit()
    conn.close()
