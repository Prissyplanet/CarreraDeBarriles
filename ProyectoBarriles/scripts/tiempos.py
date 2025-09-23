import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from scriptTiempos import actualizar_competidores_por_categoria, cargar_competidores, cargar_tabla_por_categoria, verificar_afiliacion, registrar_valores, recalcular_puestos

class RegistroTiempos(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        cargar_competidores(self.competidor)

    def initUI(self):
        self.setGeometry(100, 100, 1920, 1080)
        self.setWindowTitle("Registro de Tiempos")
        self.setStyleSheet("background-color: #FEC200;")  

        
        base_path = os.path.dirname(os.path.abspath(__file__))
        back_path = os.path.join(base_path, '..', 'img', 'back.png')

      
        self.back_image = QLabel(self)
        pixmap = QPixmap(back_path)
        self.back_image.setPixmap(pixmap)
        self.back_image.setGeometry(30, 30, 60, 60)  
        self.back_image.setCursor(Qt.PointingHandCursor)  
        self.back_image.mousePressEvent = self.on_back_click

        
        logo_path = os.path.join(base_path, '..', 'img', 'logo.svg')
        self.logo = QLabel(self)
        pixmap_logo = QPixmap(logo_path).scaled(200, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap_logo)
        self.logo.setGeometry(1700, 30, 200, 70)

        
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

        layout = QVBoxLayout(self.container)

        self.title = QLabel("Registro de tiempos", self.container)
        self.title.setStyleSheet("font-family: Arial; font-size: 60px; font-weight: regular; color: black;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.categoria = QComboBox(self.container)
        self.categoria.addItems(["Selecciona una categoría", "Infantil", "Juvenil", "Abierta"])  
      
        layout.addWidget(self.categoria, alignment=Qt.AlignRight)

        self.competidor = QComboBox(self.container)
        self.estilizar_combobox(self.competidor)
        self.competidor.setEnabled(False)
        layout.addWidget(self.competidor)

        self.categoria.currentTextChanged.connect(self.on_categoria_changed)  

        self.competidor.currentTextChanged.connect(lambda: verificar_afiliacion(self.competidor.currentText(), self.puntos))


        self.tiempo = QLineEdit(self.container)
        self.tiempo.setPlaceholderText("Registrar tiempo")
        self.estilizar_input(self.tiempo)
        layout.addWidget(self.tiempo)

        self.puntos = QLineEdit(self.container)
        self.puntos.setPlaceholderText("Registrar puntos")
        self.estilizar_input(self.puntos)
        layout.addWidget(self.puntos)

        self.table = QTableWidget(self.container)
        self.table.setRowCount(10)  
        self.table.setColumnCount(8)  # Columnas
        self.table.setHorizontalHeaderLabels(["Nombre", "Caballo", "Lugar", "Tiempo", "Puesto", "Puntos", "Categoría", "División"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Botones debajo de la tabla
        button_layout = QHBoxLayout()
        self.exportar_button = QPushButton("Exportar tabla", self.container)
        self.estilizar_boton(self.exportar_button)
        button_layout.addWidget(self.exportar_button, alignment=Qt.AlignLeft)

        self.registrar_button = QPushButton("Registrar", self.container)
        self.estilizar_boton(self.registrar_button)
        button_layout.addWidget(self.registrar_button, alignment=Qt.AlignRight)
        self.registrar_button.clicked.connect(self.registrar_tiempo)

        layout.addLayout(button_layout)
        self.show()

    def on_categoria_changed(self, categoria):
        """Actualiza la tabla y combobox al cambiar de categoría."""
        if categoria == "Selecciona una categoría":
            self.competidor.clear()
            self.competidor.addItem("Selecciona un competidor")
            self.competidor.setEnabled(False)
            self.table.setRowCount(0)  # Limpia la tabla
        else:
            cargar_tabla_por_categoria(categoria, self.table)
            cargar_competidores(self.competidor, categoria)  # Se envía la categoría

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

    def estilizar_boton(self, boton):
        boton.setStyleSheet("""
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
    def registrar_tiempo(self):
        """
        Registra el tiempo y los puntos en la base de datos para el competidor seleccionado.
        """
        competidor = self.competidor.currentText()
        tiempo = self.tiempo.text()
        puntos = self.puntos.text()

        # Validar que se haya seleccionado un competidor válido
        if competidor == "Selecciona un competidor":
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar un competidor.")
            return

        # Validar que se haya ingresado un tiempo
        if not tiempo:
            QMessageBox.warning(self, "Advertencia", "Debes registrar un tiempo.")
            return

        # Validar formato del tiempo (número decimal)
        try:
            tiempo_float = float(tiempo)
            if tiempo_float <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "El tiempo debe ser un número positivo.")
            return

        # Registrar los valores en la base de datos
        if registrar_valores(competidor, tiempo, puntos):
            QMessageBox.information(self, "Éxito", "Tiempo y puntos registrados correctamente.")
            # Actualizar la tabla
            self.on_categoria_changed(self.categoria.currentText())
        else:
            QMessageBox.critical(self, "Error", "No se pudieron registrar los valores.")

        if registrar_valores(competidor, tiempo, puntos):
            recalcular_puestos(self.categoria.currentText())  # Recalcular puestos para la categoría actual
            QMessageBox.information(self, "Éxito", "Tiempo, puntos y puestos actualizados correctamente.")
            self.on_categoria_changed(self.categoria.currentText())  # Actualizar la tabla
        else:
            QMessageBox.critical(self, "Error", "No se pudieron registrar los valores.")

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
            self.abrirCompetidores()

    def abrirCompetidores(self):
        from competidor import RegistroCompetidores
        self.RegistroCompetidores=RegistroCompetidores()
        self.RegistroCompetidores.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistroTiempos()
    sys.exit(app.exec_())


