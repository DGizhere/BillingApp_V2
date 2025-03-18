# Billing App V2 (PySide + MySQL)

A simple desktop-based billing application built using **PySide** for the GUI and **MySQL** for local database storage. This application allows users to generate and store bills, retrieve past records, and manage customer data efficiently.

## Features
- **Bill Entry Form**: Store customer and billing data.
- **Search Bills**: Filter past bills by customer name or date.
- **Dark Mode Toggle**: Switch between light and dark themes dynamically.
- **Data Validation**: Prevent empty inputs or incorrect data formats.
- **Backup & Restore**: Save and restore MySQL data as `.sql` files.

## Installation Guide
### Prerequisites
Make sure you have the following installed:
- Python 3.13.2
- MySQL Server
- Required Python libraries

### Step 1: Clone the Repository
```bash
git clone https://github.com/DGizhere/BillingApp_V2.git
cd billing-app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database
1. Create a MySQL database:
   ```sql
   CREATE DATABASE billing_db;
   ```
2. Import the schema (if provided):
   ```bash
   mysql -u root -p billing_db < database_schema.sql
   ```

### Step 4: Run the Application
```bash
python main.py
```

## Usage
- **Adding a Bill**: Enter customer details and bill information, then click 'Save'.
- **Searching for Bills**: Use the search feature to find bills by customer name or date.
- **Enabling Dark Mode**: Toggle dark mode for better readability.
- **Backing Up Database**: Save `.sql` backups via the backup feature.
- **Restoring Database**: Load previous backups when needed.

## Database Structure
Tables:
- `customers`: Stores customer details.
- `bills`: Stores billing records.

## Contributing
Feel free to fork this repository and submit pull requests with improvements!

## License
This project is open-source and available under the [MIT License](LICENSE).

## ScreenShot
![image](https://github.com/user-attachments/assets/9422cff7-fb9c-4199-ba8e-a7503e24acd0)
