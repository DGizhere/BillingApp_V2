
DROP DATABASE IF EXISTS billing_db;

CREATE DATABASE IF NOT EXISTS billing_db;
-- Switch to the correct database
USE billing_db;

-- Drop the table if it exists (to avoid conflicts)
DROP TABLE IF EXISTS bills;

-- Recreate the table with correct column names
CREATE TABLE if NOT EXISTS bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    bill_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bill_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    amount DECIMAL(10,2) GENERATED ALWAYS AS (unit_price * quantity) STORED,
    FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE
);


-- Create index on phone_number (should work now)
ALTER TABLE bills ADD INDEX idx_phone (phone_number);

-- Insert sample data (optional)
INSERT INTO bills (customer_name, phone_number, bill_amount) 
VALUES 
('Aman Mishra', '9876543210', 1200.50),
('Zoro Senpai', '9123456789', 2500.75);

DESC bills;
DESC bill_items;
```
This code will create the `bills` and `bill_items` tables with the correct column names and data types. It will also add an index on the `phone_number` column to improve query performance. Finally, it will insert some sample data into the `bills` table.
