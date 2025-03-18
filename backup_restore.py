import subprocess
from PySide6.QtWidgets import QFileDialog, QMessageBox

class BackupRestore:
    def __init__(self, parent, db_name, db_user, db_password):
        self.parent = parent
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def backup_database(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Backup", "", "SQL Files (*.sql)", options=options)
        if file_name:
            try:
                command = f"mysqldump -u {self.db_user} -p{self.db_password} {self.db_name} > \"{file_name}\""
                subprocess.run(command, shell=True, check=True)
                QMessageBox.information(self.parent, "Backup Successful", f"Backup saved to: {file_name}")
            except subprocess.CalledProcessError:
                QMessageBox.warning(self.parent, "Backup Failed", "Failed to create backup. Please check MySQL setup.")

    def restore_database(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Select Backup File", "", "SQL Files (*.sql)", options=options)
        if file_name:
            try:
                command = f"mysql -u {self.db_user} -p{self.db_password} {self.db_name} < \"{file_name}\""
                subprocess.run(command, shell=True, check=True)
                QMessageBox.information(self.parent, "Restore Successful", f"Database restored from: {file_name}")
            except subprocess.CalledProcessError:
                QMessageBox.warning(self.parent, "Restore Failed", "Failed to restore database. Please check MySQL setup.")
# End of snippet from BillingApp_V2/backup_restore.py