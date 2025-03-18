import mysql.connector

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",    # Replace with your MySQL password
    "database": "billing_db"
}

def execute_schema():
    """Creates the necessary tables for the billing system"""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Create Customers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(15) UNIQUE NOT NULL
        )
    """)

    # Create Bills Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            total_amount DECIMAL(10,2) NOT NULL,
            bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
        )
    """)

    print("Database tables created successfully!")

    connection.commit()
    cursor.close()
    connection.close()

# Run Table Creation
if __name__ == "__main__":
    execute_schema()

