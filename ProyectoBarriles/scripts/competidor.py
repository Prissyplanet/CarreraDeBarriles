import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from scriptCompetidor import registrar_competidor  
from login import LoginWindow
from tiempos import RegistroTiempos


class RegistroCompetidores(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana principal
        self.setGeometry(100, 100, 1920, 1080)
        self.setWindowTitle("Registro de Competidores")
        self.setStyleSheet("background-color: #FEC200;")  # Fondo amarillo

        # Ruta para la imagen del botón "Back"
        base_path = os.path.dirname(os.path.abspath(__file__))
        back_path = os.path.join(base_path, '..', 'img', 'back.png')

        # Verificar si la imagen existe
        if not os.path.exists(back_path):
            print(f"ERROR: La imagen no se encuentra en la ruta: {back_path}")
        else:
            print(f"Imagen 'Back' encontrada en la ruta: {back_path}")

        # Cargar la imagen con QPixmap
        self.back_image = QLabel(self)
        pixmap = QPixmap(back_path)
        if pixmap.isNull():
            print("ERROR: No se pudo cargar la imagen 'Back'.")
        else:
            print("Imagen 'Back' cargada correctamente.")

        # Establecer la imagen en el QLabel
        self.back_image.setPixmap(pixmap)
        self.back_image.setGeometry(30, 30, 60, 60)  # Tamaño y posición de la imagen
        self.back_image.setCursor(Qt.PointingHandCursor)  # Cambia el cursor cuando pasa sobre la imagen

        # Conectar el clic a un evento
        self.back_image.mousePressEvent = self.on_back_click
        

        # Logo en la parte superior derecha
        logo_path = os.path.join(base_path, '..', 'img', 'logo.png')
        self.logo = QLabel(self)
        pixmap_logo = QPixmap(logo_path).scaled(200, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap_logo)
        self.logo.setGeometry(1700, 30, 200, 70)

        # Contenedor blanco
        container_width = 1800
        container_height = 800
        center_x = (1920 - container_width) // 2
        center_y = (1080 - container_height) // 2
        self.container = QWidget(self)
        self.container.setGeometry(center_x, center_y, container_width, container_height)
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 25px;
        """)

        # Layout del contenedor
        layout = QVBoxLayout(self.container)

        # Título
        self.title = QLabel("Registro de competidores", self.container)
        self.title.setStyleSheet("font-family: Arial; font-size: 60px; font-weight: regular; color: black;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Inputs y selectbox
        self.nombre = QLineEdit(self.container)
        self.nombre.setPlaceholderText("Nombre")
        self.estilizar_input(self.nombre)
        layout.addWidget(self.nombre)

        self.caballo = QLineEdit(self.container)
        self.caballo.setPlaceholderText("Caballo")
        self.estilizar_input(self.caballo)
        layout.addWidget(self.caballo)

        self.lugar = QLineEdit(self.container)
        self.lugar.setPlaceholderText("Lugar")
        self.estilizar_input(self.lugar)
        layout.addWidget(self.lugar)

        self.categoria = QComboBox(self.container)
        self.categoria.addItems(["Selecciona una categoría", "Abierta", "Juvenil", "Infantil"])
        self.estilizar_combobox(self.categoria)
        layout.addWidget(self.categoria)

        self.division = QComboBox(self.container)
        self.division.addItems(["Selecciona una división", "Primera", "Segunda", "Tercera", "Cuarta", "Quinta", "Sexta"])
        self.estilizar_combobox(self.division)
        layout.addWidget(self.division)

        self.afiliado = QComboBox(self.container)
        self.afiliado.addItems(["Selecciona afiliación", "AFILIADO", "NO AFILIADO"])
        self.estilizar_combobox(self.afiliado)
        layout.addWidget(self.afiliado)

        # Botón de "Registrar"
        self.registrar_button = QPushButton("Registrar", self.container)
        self.registrar_button.setStyleSheet("""
            QPushButton {
                background-color: #ED1B24;
                color: white;
                font-size: 20px;
                padding: 12px 24px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #C81A1F;
            }
        """)
        self.registrar_button.clicked.connect(self.on_register_click)
        layout.addWidget(self.registrar_button, alignment=Qt.AlignCenter)

        # Botón de "Tiempos"
        self.tiempos_button = QPushButton("Tiempos", self)
        self.tiempos_button.setStyleSheet("""
            QPushButton {
                background-color: #ED1B24;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #C81A1F;
            }
        """)
        self.tiempos_button.clicked.connect(self.on_time_click)
        tiempos_layout = QHBoxLayout()
        tiempos_layout.addStretch()
        tiempos_layout.addWidget(self.tiempos_button)
        layout.addLayout(tiempos_layout)

        self.show()

    def on_register_click(self):
        """Método que se llama cuando se hace clic en el botón registra"""
        nombre = self.nombre.text().strip()
        caballo = self.caballo.text().strip()
        lugar = self.lugar.text().strip()
        categoria = self.categoria.currentText()
        division = self.division.currentText()
        afiliado = self.afiliado.currentText()

        if not nombre or not caballo or not lugar or categoria == "Selecciona una categoría" or division == "Selecciona una división" or afiliado == "Selecciona afiliación":
                print("Por favor, complete todos los campos antes de registrar.")
                return  # No procede si los campos están vacíos

        #Llamar a la función
        registrar_competidor(nombre, caballo, lugar, categoria, division, afiliado)

        #Limpiar campos
        self.nombre.clear()
        self.caballo.clear()
        self.lugar.clear()
        self.categoria.setCurrentIndex(0) 
        self.division.setCurrentIndex(0) 
        self.afiliado.setCurrentIndex(0) 

    def on_back_click(self, event):

        reply = QMessageBox.question(
            self,
            'Confirmar salida',
            '¿Estás seguro de que quieres salir de la ventana actual?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            self.abrirLogin()

    def abrirLogin(self):
        self.loginWindow=LoginWindow()
        self.loginWindow.show()
        
    def on_time_click(self,event):
        reply = QMessageBox.question(
            self,
            'Confirmar salida',
            '¿Estás seguro de que quieres salir de la ventana actual e ir al registro de tiempos?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            self.abrirTiempos()
    
    def abrirTiempos(self):
        self.RegistroTiempos=RegistroTiempos()
        self.RegistroTiempos.show()


    def estilizar_input(self, input_field):
        input_field.setStyleSheet("""
            font-family: Calibri;
            font-size: 22px;
            padding: 10px;
            border: 1px solid gray;
            border-radius: 5px;
        """)

    def estilizar_combobox(self, combobox):
        combobox.setStyleSheet("""
            QComboBox {
                font-family: Calibri;
                font-size: 22px;
                padding: 10px;
                border: 1px solid gray;
                border-radius: 5px;
                background-color: white;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistroCompetidores()
    sys.exit(app.exec_())
