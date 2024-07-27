# page.py
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QFileDialog, QMessageBox, QLineEdit, QHBoxLayout, QFormLayout, QLabel
)
from PyQt5.QtCore import Qt
from appExportaFirebase.firebase_service import FirebaseService  # Certifique-se de que isso está correto

class Page(QWidget):
    def __init__(self, firebase_service):
        super().__init__()
        self.firebase_service = firebase_service

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Licenças")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.filter_layout = QHBoxLayout()
        self.email_filter = QLineEdit()
        self.email_filter.setPlaceholderText("Filtro email...")
        self.filter_layout.addWidget(self.email_filter)
        self.code_filter = QLineEdit()
        self.code_filter.setPlaceholderText("Filtro code...")
        self.filter_layout.addWidget(self.code_filter)
        self.status_filter = QLineEdit()
        self.status_filter.setPlaceholderText("Filtro status...")
        self.filter_layout.addWidget(self.status_filter)
        self.filter_button = QPushButton("Filtrar")
        self.filter_layout.addWidget(self.filter_button)
        self.layout.addLayout(self.filter_layout)

        self.export_button = QPushButton("Exportar CSV")
        self.layout.addWidget(self.export_button)

        self.filter_button.clicked.connect(self.apply_filters)
        self.export_button.clicked.connect(self.export_to_csv)

        self.load_data()

    def load_data(self):
        if not self.firebase_service.is_connected():
            QMessageBox.critical(self, "Error", "Não conectado Firebase")
            return
        
        self.data = self.firebase_service.get_licenses()
        self.original_data = self.data.copy()
        self.update_table()

    def update_table(self):
        if not self.data:
            return
        
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Email Activation", "Status", "Code"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, entry in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get('email_ativacao', '')))
            self.table.setItem(row, 1, QTableWidgetItem(entry.get('status', '')))
            self.table.setItem(row, 2, QTableWidgetItem(entry.get('code', '')))

    def apply_filters(self):
        email_filter = self.email_filter.text().lower()
        code_filter = self.code_filter.text().lower()
        status_filter = self.status_filter.text().lower()

        if not email_filter and not code_filter and not status_filter:
            self.data = self.original_data
        else:
            self.data = [entry for entry in self.original_data
                         if (email_filter in entry.get('email_ativacao', '').lower() and
                             code_filter in entry.get('code', '').lower() and
                             status_filter in entry.get('status', '').lower())]

        self.update_table()

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not file_path:
            return

        df = pd.DataFrame(self.data)
        try:
            df.to_csv(file_path, index=False)
            QMessageBox.information(self, "Success", "Data exported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting data: {e}")
