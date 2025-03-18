import sys
import mysql.connector
from search_bills import SearchBills
from backup_restore import BackupRestore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QMessageBox
    )
from PySide6.QtGui import QFont

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # Replace with your actual MySQL password
    "database": "billing_db"
}

class BillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window Properties
        self.setWindowTitle("Billing Application")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #222; color: white;")
        # Main Widget and Layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        # Customer Details Section
        self.label_name = QLabel("Customer Name:")
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Enter customer name")
        self.label_phone = QLabel("Phone Number:")
        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Enter phone number")
        # Item Details Section
        self.item_name_label = QLabel("Item Name:")
        self.item_name_input = QLineEdit()
        self.unit_price_label = QLabel("Unit Price:")
        self.unit_price_input = QLineEdit()
        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.clicked.connect(self.add_item_to_table)
        # Item Table
        self.item_table = QTableWidget()
        self.item_table.setColumnCount(4)
        self.item_table.setHorizontalHeaderLabels(["Item Name", "Unit Price", "Quantity", "Amount"])
        self.item_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Bill Amount
        self.label_amount = QLabel("Total Bill Amount:")
        self.input_amount = QLineEdit()
        self.input_amount.setReadOnly(True)
        # Buttons
        self.button_save = QPushButton("Save Bill")
        self.button_show = QPushButton("Show Bills")
        self.button_delete = QPushButton("Delete Bill")
        self.backup_button = QPushButton("Backup Database")
        self.restore_button = QPushButton("Restore Database")
        # Output Area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        # Styling Widgets
        for widget in [self.input_name, self.input_phone, self.input_amount, self.output_area]:
            widget.setStyleSheet("background-color: #333; color: white; padding: 5px; border-radius: 5px;")
        for btn in [self.button_save, self.button_show, self.button_delete, self.add_item_button]:
            btn.setStyleSheet("background-color: #555; color: white; padding: 8px; border-radius: 5px;")
            btn.setFont(QFont("Arial", 10, QFont.Bold))
        # Add Widgets to Layout
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.input_name)
        self.layout.addWidget(self.label_phone)
        self.layout.addWidget(self.input_phone)
        self.layout.addWidget(self.item_name_label)
        self.layout.addWidget(self.item_name_input)
        self.layout.addWidget(self.unit_price_label)
        self.layout.addWidget(self.unit_price_input)
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(self.add_item_button)
        self.layout.addWidget(self.item_table)
        self.layout.addWidget(self.label_amount)
        self.layout.addWidget(self.input_amount)
        self.layout.addWidget(self.button_save)
        self.layout.addWidget(self.button_show)
        self.layout.addWidget(self.button_delete)
        self.layout.addWidget(self.output_area)
        self.layout.addWidget(self.backup_button)
        self.layout.addWidget(self.restore_button)
        # Set Layout
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.button_save.clicked.connect(self.save_bill)
        self.button_show.clicked.connect(self.show_bills)
        self.button_delete.clicked.connect(self.delete_bill)
        self.backup_restore = BackupRestore(self, "localhost","root", "1234")
        self.backup_button.clicked.connect(self.backup_restore.backup_database)
        self.restore_button.clicked.connect(self.backup_restore.restore_database)
        self.input_amount.setStyleSheet("background-color: #444; color: #FFD700; padding: 5px; border-radius: 5px; font-weight: bold;")
        # Search Bills
        self.db_config = DB_CONFIG  # ✅ Use the correct global config
        self.search_window = SearchBills(self.db_config)
        self.search_button = QPushButton("Search Bills")
        self.search_button.clicked.connect(self.search_window.show)
        self.layout.addWidget(self.search_button)  # ✅ Add the button properly

    def connect(self):
        """Establish a database connection."""
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect: {e}")
            return None

    def validate_inputs(self):
        # Get input values
        customer_name = self.input_name.text().strip()
        phone_number = self.input_phone.text().strip()
        price = self.unit_price_input.text().strip()
        quantity = self.quantity_input.text().strip()
        # Validate Customer Name (Only letters and spaces)
        if not customer_name.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Validation Error", "Customer name must contain only letters.")
            return False
        # Validate Phone Number (Only digits & exactly 10 digits)
        if not phone_number.isdigit() or len(phone_number) != 10:
            QMessageBox.warning(self, "Validation Error", "Phone number must be exactly 10 digits.")
            return False
        # Validate Price (Must be a valid number and greater than zero)
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Price must be a valid number greater than zero.")
            return False
        # Validate Quantity (Must be an integer and greater than zero)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Quantity must be a whole number greater than zero.")
            return False
        return True  # If all validations pass

    def save_bill(self):
        customer_name = self.input_name.text().strip()
        phone_number = self.input_phone.text().strip()
        if not customer_name or not phone_number:
            QMessageBox.warning(self, "Input Error", "Please enter customer details.")
            return
        try:
            connection = self.connect()
            if not connection:
                return    # Exit if the connection fails
            cursor = connection.cursor()
            # Insert Bill
            cursor.execute("INSERT INTO bills (customer_name, phone_number, bill_amount) VALUES (%s, %s, 0)",
                           (customer_name, phone_number))
            bill_id = cursor.lastrowid  # Get the inserted bill ID
            # Insert Items
            total_bill_amount = 0
            for row in range(self.item_table.rowCount()):
                item_name = self.item_table.item(row, 0).text()
                unit_price = float(self.item_table.item(row, 1).text())
                quantity = int(self.item_table.item(row, 2).text())
                cursor.execute("INSERT INTO bill_items (bill_id, item_name, unit_price, quantity) VALUES (%s, %s, %s, %s)",
                               (bill_id, item_name, unit_price, quantity))
                total_bill_amount += unit_price * quantity
            # Update total bill amount
            cursor.execute("UPDATE bills SET bill_amount = %s WHERE id = %s", (total_bill_amount, bill_id))
            connection.commit()
            QMessageBox.information(self, "Success", "Bill saved successfully!")
            self.input_name.clear()
            self.input_phone.clear()
            self.item_table.setRowCount(0)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save bill: {e}")
        try:
            cursor = connection.cursor()
            ...
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_bills(self):
        """Fetch and display all saved bills."""
        try:
            connection = self.connect()
            if not connection:
                return
            cursor = connection.cursor()
            cursor.execute("SELECT id, customer_name, phone_number, bill_amount FROM bills")

            bills = cursor.fetchall()
            if not bills:
                self.output_area.setText("No bills found.")
                return
            # Display bills in the output area
            output_text = "Saved Bills:\n"
            for bill in bills:
                output_text += f"ID: {bill[0]}, Name: {bill[1]}, Phone: {bill[2]}, Amount: ₹{bill[3]:.2f}\n"
            self.output_area.setText(output_text)
            cursor.close()
            connection.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch bills: {e}")

    def delete_bill(self):
        """Deletes a bill based on the phone number."""
        phone = self.input_phone.text().strip()
        if not phone:
            QMessageBox.warning(self, "Input Error", "Please enter a phone number to delete a bill.")
            return
        try:
            connection = self.connect()
            if not connection:
                return
            cursor = connection.cursor()
            cursor.execute("DELETE FROM bill_items WHERE bill_id IN (SELECT id FROM bills WHERE phone_number = %s)", (phone,))
            cursor.execute("DELETE FROM bills WHERE phone_number = %s", (phone,))
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Not Found", "No bill found for this phone number.")
                return
            connection.commit()
            connection.close()
            QMessageBox.information(self, "Success", f"Bills associated with phone {phone} deleted.")
            self.show_bills()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error deleting bill: {e}")

    def add_item_to_table(self):
        item_name = self.item_name_input.text().strip()
        unit_price = self.unit_price_input.text().strip()
        quantity = self.quantity_input.text().strip()
        if not item_name or not unit_price or not quantity:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return
        try:
            unit_price = float(unit_price)
            quantity = int(quantity)
            amount = unit_price * quantity
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Enter valid numbers for price and quantity.")
            return
        row_position = self.item_table.rowCount()
        self.item_table.insertRow(row_position)
        self.item_table.setItem(row_position, 0, QTableWidgetItem(item_name))
        self.item_table.setItem(row_position, 1, QTableWidgetItem(f"{unit_price:.2f}"))
        self.item_table.setItem(row_position, 2, QTableWidgetItem(str(quantity)))
        self.item_table.setItem(row_position, 3, QTableWidgetItem(f"{amount:.2f}"))
        # Clear input fields
        self.item_name_input.clear()
        self.unit_price_input.clear()
        self.quantity_input.clear()
        # Update total amount in real-time
        self.update_total_amount()

    def update_total_amount(self):
        total = 0
        for row in range(self.item_table.rowCount()):
            amount_item = self.item_table.item(row, 3)  # Amount column
            if amount_item:
                total += float(amount_item.text())  # Convert to float and add

        self.input_amount.setText(f"{total:.2f}")  # Update total bill amount display

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
# End of BillingApp_V2/main.py
# Compare this snippet from BillingApp_V2/search_bills.py: