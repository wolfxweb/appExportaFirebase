# firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    def __init__(self, config_file):
        self.connected = False
        try:
            # Inicialize o Firebase
            self.cred = credentials.Certificate(config_file)
            firebase_admin.initialize_app(self.cred)
            # Inicialize o Firestore
            self.db = firestore.client()
            self.connected = True
        except Exception as e:
            print(f"An error occurred while connecting to Firebase: {e}")
            self.connected = False

    def get_licenses(self):
        if not self.connected:
            return []
        try:
            licenses_ref = self.db.collection('licenses')
            docs = licenses_ref.stream()
            licenses = [doc.to_dict() for doc in docs]
            print(f"Licenses retrieved: {licenses}")  # Debug print
            return licenses
        except Exception as e:
            print(f"Errorß: {e}")
            return []

    def is_connected(self):
        return self.connected
    
    def get_dados_basicos(self):
        if not self.connected:
            return []
        try:
            licenses_ref = self.db.collection('dados_basicos')
            docs = licenses_ref.stream()
            licenses = [doc.to_dict() for doc in docs]
            print(f"Dados básicos: {licenses}")  # Debug print
            return licenses
        except Exception as e:
            print(f"Error : {e}")
            return []