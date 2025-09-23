import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from login import LoginWindow
from db_connection import create_connection  

class App:
    def __init__(self):
        self.window = LoginWindow()
        self.window.login_button.clicked.connect(self.registrar_usuario)

    def registrar_usuario(self):
        username = self.window.username.text()
        password = self.window.password.text()

        print("Datos recibidos para registro:", username, password)

        
        if not username or not password:
            print("Advertencia: campos vacíos") 
            QMessageBox.warning(self.window, 'Error', 'Por favor, llena ambos campos.')
            return

        connection = None
        cursor = None
        try:
            print("Intentando conectar a la base de datos...")  # Mensaje de depuración
            # Conectar a la base de datos
            connection = create_connection()  # Usa la conexión importada

            if connection.is_connected():
                print("Conexión a la base de datos establecida.")  # Mensaje de depuración
            else:
                print("No se pudo conectar a la base de datos.")  # Mensaje de depuración
                QMessageBox.critical(self.window, 'Error', 'No se pudo conectar a la base de datos.')
                return

            cursor = connection.cursor()

            # Insertar usuario en la tabla
            query = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()
            print("Usuario registrado en la base de datos.")  # Mensaje de depuración

            QMessageBox.information(self.window, 'Registro', 'Usuario registrado exitosamente!')

        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            QMessageBox.critical(self.window, 'Error', f'Ocurrió un error: {e}')

        finally:
            if cursor:
                cursor.close()
                print("Cursor cerrado.")  # Mensaje de depuración
            if connection and connection.is_connected():
                connection.close()
                print("Conexión a la base de datos cerrada.")  # Mensaje de depuración

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = App()
    main_app.window.show()
    sys.exit(app.exec_())
