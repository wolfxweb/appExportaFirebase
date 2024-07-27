import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QFileDialog, QMessageBox, QLineEdit, QHBoxLayout, QFormLayout, QLabel
)
from PyQt5.QtCore import Qt

class DadosBasicos(QWidget):
    def __init__(self, firebase_service):
        super().__init__()
        self.firebase_service = firebase_service

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create and add the title label
        self.title_label = QLabel("Dados Básicos")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Create a QTableWidget to display the data
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Create a filter layout and filter widgets
        self.filter_layout = QFormLayout()
        self.filter_layout.setSpacing(5)
        self.filter_layout.setLabelAlignment(Qt.AlignRight)

        # Create a button layout for filters and apply button
        self.button_layout = QHBoxLayout()
        self.filter_button = QPushButton("Filtrar")
        self.button_layout.addWidget(self.filter_button)
        self.button_layout.setSpacing(10)

        # Add filter layout and button layout to the main layout
        self.layout.addLayout(self.filter_layout)
        self.layout.addLayout(self.button_layout)

        # Create export button
        self.export_button = QPushButton("Exportar CSV")
        self.layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_to_csv)

        # Connect the filter button to the apply_filters method
        self.filter_button.clicked.connect(self.apply_filters)

        self.data = []
        self.original_data = []
        self.headers = []

        self.load_data()

    def load_data(self):
        if not self.firebase_service.is_connected():
            QMessageBox.critical(self, "Error", "Não conectado no Firebase")
            return
        
        self.data = self.firebase_service.get_dados_basicos()  # Obtém os dados básicos do Firebase
        if isinstance(self.data, dict):
            self.data = list(self.data.values())  # Converte o dicionário de dicionários em uma lista de dicionários

        self.original_data = self.data.copy()  # Guarda uma cópia dos dados originais
        self.update_table()

    def update_table(self):
        if not self.data:
            return
        
        # Set up the table with data
        self.table.setRowCount(len(self.data))
        if len(self.data) > 0:
            self.table.setColumnCount(len(self.data[0]))
            self.headers = list(self.data[0].keys())
            self.table.setHorizontalHeaderLabels(self.headers)
        else:
            self.table.setColumnCount(0)
            self.table.setHorizontalHeaderLabels([])

        # Set up filters
        self.setup_filters(self.headers)

        # Populate the table
        for row, entry in enumerate(self.data):
            for col, key in enumerate(self.headers):
                value = entry.get(key, '')
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def setup_filters(self, headers):
        # Clear existing filters
        for widget in self.filter_layout.children():
            widget.deleteLater()

        # Create filters
        self.filters = []
        num_filters_per_row = 3

        # Create filter widgets for each column
        for i, header in enumerate(headers):
            if i % num_filters_per_row == 0:
                # Create a new row layout for each set of filters
                filter_row_layout = QHBoxLayout()
                filter_row_layout.setSpacing(10)
                self.filter_layout.addRow(filter_row_layout)
            
            filter_widget = QLineEdit()
            filter_widget.setPlaceholderText(f"Filtro {header}...")
            filter_widget.setFixedWidth(250)
            filter_row_layout.addWidget(filter_widget)
            self.filters.append(filter_widget)

    def apply_filters(self):
        filters = [filter.text().lower() for filter in self.filters]
        
        if any(filters):
            filtered_data = []
            for entry in self.original_data:
                if all(filters[i] in str(value).lower() for i, value in enumerate(entry.values())):
                    filtered_data.append(entry)
            self.data = filtered_data
        else:
            # If no filters, show all data
            self.data = self.original_data

        self.update_table()

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar para CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if not file_path:
            return

        df = pd.DataFrame(self.data)
        try:
            df.to_csv(file_path, index=False)
            QMessageBox.information(self, "Sucesso", "Dados exportados com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao exportar os dados: {e}")
