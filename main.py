import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QStackedWidget, QWidget, QVBoxLayout, QPushButton
from appExportaFirebase.page_licencas import Page
from appExportaFirebase.page_dados_basicos import DadosBasicos  # Importa a nova página
from appExportaFirebase.firebase_service import FirebaseService

class MainWindow(QMainWindow):
    def __init__(self, firebase_service):
        super().__init__()

        # Inicializa o serviço Firebase
        self.firebase_service = firebase_service

        # Configura a janela principal
        self.setWindowTitle("Exportador firebase")
        self.setGeometry(100, 100, 800, 600)

        # Cria um stacked widget para gerenciar as páginas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Cria a barra de menu
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("Menu")

        # Adiciona ações ao menu
        self.licencas_action = QAction("Licenças", self)
        self.dados_basicos_action = QAction("Dados Básicos", self)
        
        self.licencas_action.triggered.connect(self.open_licencas_page)
        self.dados_basicos_action.triggered.connect(self.open_dados_basicos_page)

        self.file_menu.addAction(self.licencas_action)
        self.file_menu.addAction(self.dados_basicos_action)

        # Adiciona as páginas
        self.page_licencas = Page(self.firebase_service)
        self.page_dados_basicos = DadosBasicos(self.firebase_service)

        self.stacked_widget.addWidget(self.page_licencas)
        self.stacked_widget.addWidget(self.page_dados_basicos)

        # Define a página inicial
        self.stacked_widget.setCurrentWidget(self.page_licencas)

    def open_licencas_page(self):
        self.stacked_widget.setCurrentWidget(self.page_licencas)

    def open_dados_basicos_page(self):
        self.stacked_widget.setCurrentWidget(self.page_dados_basicos)

def main():
    app = QApplication(sys.argv)
    
    # Inicializa o FirebaseService com o caminho para o arquivo de configuração do Firebase
    firebase_service = FirebaseService('firebase-admin.json')
    
    window = MainWindow(firebase_service)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
