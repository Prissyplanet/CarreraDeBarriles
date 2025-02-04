from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from db_connection import create_connection
import sys

class RondaLargaWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Establecer título y tamaño de la ventana
        self.setWindowTitle('Ronda Larga')
        self.setGeometry(100, 100, 800, 600)
        
        # Definir colores y estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3B4E;  /* Fondo oscuro */
                color: #3B4D67;  /* Texto blanco */
            }
            QLineEdit, QComboBox {
                background-color: #3B4D67;  /* Fondo de campos de texto */
                color: #FFFFFF;  /* Texto blanco */
                border: 1px solid #4A6572;  /* Borde sutil */
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #557A95;  /* Color de los botones */
                color: white;
                border: 1px solid #4A6572;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #466D84;  /* Color al pasar el mouse */
            }
            QTableWidget {
                background-color: #3B4D67;
                border: 1px solid #4A6572;
                color: #FFFFFF;
                gridline-color: #4A6572;
            }
            QTableWidget::item {
                border: 1px solid #4A6572;
            }
            QTableWidget::horizontalHeader {
                background-color: #557A95;
            }
        """)

        self.layout = QVBoxLayout()

        # Formulario para registrar un competidor
        self.form_layout = QFormLayout()

        # Campos de entrada
        self.nombre_input = QLineEdit(self)
        self.caballo_input = QLineEdit(self)
        self.lugar_input = QLineEdit(self)
        self.tiempo_input = QLineEdit(self)
        self.puntos_input = QLineEdit(self)

        # ComboBox para categoría
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.addItems(['Abierta', 'Infantil', 'Juvenil'])

        # ComboBox para división
        self.division_combo = QComboBox(self)
        self.division_combo.addItems(['Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta', 'Sexta'])

        # Botón de registrar
        self.registrar_button = QPushButton('Registrar Competidor', self)
        self.registrar_button.clicked.connect(self.registrar_competidor)

        # Agregar los campos al formulario
        self.form_layout.addRow('Nombre:', self.nombre_input)
        self.form_layout.addRow('Caballo:', self.caballo_input)
        self.form_layout.addRow('Lugar:', self.lugar_input)
        self.form_layout.addRow('Tiempo:', self.tiempo_input)
        self.form_layout.addRow('Puntos:', self.puntos_input)
        self.form_layout.addRow('Categoría:', self.categoria_combo)
        self.form_layout.addRow('División:', self.division_combo)
        self.form_layout.addRow('', self.registrar_button)

        self.layout.addLayout(self.form_layout)

        # Tabla para mostrar competidores
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(8)  # Se agrega una columna más para "Campeón"
        self.table.setHorizontalHeaderLabels(['Nombre', 'Caballo', 'Lugar', 'Tiempo', 'Puesto', 'Puntos', 'Categoría', 'División'])
        
        # Agregar la tabla al layout
        self.layout.addWidget(self.table)

        # Agregar un botón para actualizar la tabla
        self.actualizar_button = QPushButton('Actualizar Tabla', self)
        self.actualizar_button.clicked.connect(self.actualizar_tabla)

        # Agregar el botón de actualizar la tabla al layout
        self.layout.addWidget(self.actualizar_button)

        self.setLayout(self.layout)

    def registrar_competidor(self):
        # Obtener los datos del formulario
        nombre = self.nombre_input.text()
        caballo = self.caballo_input.text()
        lugar = self.lugar_input.text()
        tiempo = self.tiempo_input.text()
        puntos = self.puntos_input.text()
        categoria = self.categoria_combo.currentText()
        division = self.division_combo.currentText()

        # Validar los campos
        if not nombre or not caballo or not lugar or not tiempo or not puntos:
            print("Todos los campos son obligatorios.")
            return

        # Convertir el tiempo y puntos a tipo float para cálculos
        try:
            tiempo = float(tiempo)
            puntos = int(puntos)
        except ValueError:
            print("Tiempo o puntos no válidos.")
            return

        # Crear conexión con la base de datos
        connection = create_connection()
        if connection is None:
            print("No se pudo conectar a la base de datos.")
            return

        try:
            cursor = connection.cursor()

            # Insertar el competidor en la base de datos
            query = """INSERT INTO ronda_larga (nombre, caballo, lugar, tiempo, puntos, categoria, division)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (nombre, caballo, lugar, tiempo, puntos, categoria, division))
            connection.commit()

            print("Competidor registrado exitosamente.")

            # Obtener todos los competidores para la categoría y división, ordenados por tiempo
            query_select = """SELECT id, nombre, caballo, tiempo FROM ronda_larga
                            WHERE categoria = %s AND division = %s ORDER BY tiempo ASC"""
            cursor.execute(query_select, (categoria, division))
            competidores = cursor.fetchall()

            # Asignar los puestos de campeón según el tiempo (el primero tiene el menor tiempo)
            for i, competidor in enumerate(competidores):
                competidor_id = competidor[0]
                puesto = i + 1  # El puesto es el índice + 1 (1 para el mejor tiempo, 2 para el segundo, etc.)

                # Actualizar el puesto del campeón en la base de datos
                query_update = """UPDATE ronda_larga SET puesto = %s WHERE id = %s"""
                cursor.execute(query_update, (puesto, competidor_id))

            connection.commit()

            # Refrescar la tabla de la interfaz
            self.actualizar_tabla()

        except Exception as e:
            print(f"Error al registrar el competidor: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def actualizar_tabla(self):
        # Limpia la tabla antes de llenarla
        self.table.setRowCount(0)

        # Crear conexión con la base de datos
        connection = create_connection()
        if connection is None:
            print("No se pudo conectar a la base de datos.")
            return

        try:
            cursor = connection.cursor()
            query = """SELECT nombre, caballo, lugar, tiempo, puesto, puntos, categoria, division FROM ronda_larga"""
            cursor.execute(query)
            competidores = cursor.fetchall()

            for row_position, competidor in enumerate(competidores):
                self.table.insertRow(row_position)
                for col_position, data in enumerate(competidor):
                    self.table.setItem(row_position, col_position, QTableWidgetItem(str(data)))

        except Exception as e:
            print(f"Error al actualizar la tabla: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RondaLargaWindow()
    window.show()
    sys.exit(app.exec_())
