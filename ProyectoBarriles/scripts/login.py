import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1920, 1080)  
        self.setWindowTitle('Carrera de Barriles')
        self.setStyleSheet("background-color: #FEC200;")  

        
        self.logo = QLabel(self)
        logo_path = os.path.join(os.path.dirname(__file__),'..','img', 'logo.svg')  
        pixmap = QPixmap(logo_path)

        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen desde {logo_path}")
        else:
            self.logo.setPixmap(pixmap)
            self.logo.setGeometry(100, 50, pixmap.width(), pixmap.height())  # Posición del logo
        
        # Recuadro blanco
        self.container = QWidget(self)
        self.container.setGeometry(760, 250, 500, 600)  # Posicionando el recuadro en el centro
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)

        # Layout para los elementos dentro del recuadro blanco
        vbox = QVBoxLayout()

        # Título "Iniciar Sesión"
        self.title = QLabel('Iniciar Sesión', self)
        self.title.setStyleSheet("font-family: 'Arial'; font-size: 60px; font-weight: regular; color: black;")
        self.title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.title)

        # Campo de nombre de usuario
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Nombre de usuario')
        self.username.setStyleSheet("""
            font-family: 'Calibri'; 
            font-size: 22px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid gray;
            margin-bottom: 20px;
        """)
        vbox.addWidget(self.username)

        # Campo de contraseña
        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Contraseña')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            font-family: 'Calibri'; 
            font-size: 22px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid gray;
        """)
        vbox.addWidget(self.password)

        # Checkbox para mostrar contraseña
        self.show_password = QCheckBox('Mostrar contraseña', self)
        self.show_password.stateChanged.connect(self.toggle_password_visibility)
        vbox.addWidget(self.show_password)

        # Botón "Iniciar Sesión"
        self.login_button = QPushButton('Iniciar Sesión', self)
        self.login_button.setStyleSheet("""
            background-color: #ED1B24;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            margin-top: 20px;
        """)
        vbox.addWidget(self.login_button)  # Asegúrate de añadirlo al layout

        # Enlaces de "Olvidé mi contraseña/Usuario" y "Registrarse"
        self.links = QLabel('<span style="color: gray;">Olvidé mi </span>''<a href="#" style="color: #1077C5; text-decoration: none;">contraseña </a>', self)
        self.links.setStyleSheet("font-family: 'Calibri'; font-size: 18px; margin-bottom: 20px; margin-top: 20px;")
        self.links.setAlignment(Qt.AlignCenter)
        self.links.setOpenExternalLinks(True)
        vbox.addWidget(self.links)

        self.register_link = QLabel('<span style="color: gray;">¿No tienes una cuenta? </span>''<a href="#" style="color: #1077C5; text-decoration: none;">Registrarse </a>', self)
        self.register_link.setStyleSheet("font-family: 'Calibri'; font-size: 18px; margin-bottom: 20px; margin-top: 20px;")
        self.register_link.setAlignment(Qt.AlignCenter)
        self.register_link.setOpenExternalLinks(True)
        vbox.addWidget(self.register_link)

        # Agregar el layout al contenedor (recuadro blanco)
        self.container.setLayout(vbox)

        self.show()
    
    def toggle_password_visibility(self, state):
        """MUESTRA U OCULTA LA CONTRASEÑA"""
        if state == Qt.Checked:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())