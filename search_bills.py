from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
import mysql.connector

class SearchBills(QWidget):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.setWindowTitle("Search Bills")
        self.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()
        self.label_name = QLabel("Search by Customer Name:")
        self.input_name = QLineEdit()
        self.label_date = QLabel("Search by Date (YYYY-MM-DD):")
        self.input_date = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_bills)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Bill ID", "Customer Name", "Date", "Total Amount"])
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_date)
        layout.addWidget(self.input_date)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_table)
        self.setLayout(layout)

    def search_bills(self):
        name = self.input_name.text().strip()
        date = self.input_date.text().strip()
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        query = "SELECT bill_id, customer_name, bill_date, total_amount FROM bills WHERE 1=1"
        params = []
        if name:
            query += " AND customer_name LIKE %s"
            params.append(f"%{name}%")
        if date:
            query += " AND bill_date = %s"
            params.append(date)
        cursor.execute(query, params)
        results = cursor.fetchall()
        self.results_table.setRowCount(len(results))
        for row_idx, row_data in enumerate(results):
            for col_idx, data in enumerate(row_data):
                self.results_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        cursor.close()
        conn.close()
