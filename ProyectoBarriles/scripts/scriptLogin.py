import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from mysql.connector import connect, Error
from db_connection import create_connection  # Importar la función de conexión
from login import LoginWindow  # Asegúrate de que este nombre coincida con tu archivo de diseño
from competidor import RegistroCompetidores

class App:
    def __init__(self):
        self.window = LoginWindow()
        self.window.login_button.clicked.connect(self.login)  # Conecta el botón a la función de inicio de sesión
        print("Conexión configurada con éxito")

    def login(self):
        print("Botón de inicio de sesión clickeado")
        try:
            # Obtener datos del formulario
            username = self.window.username.text()
            password = self.window.password.text()

            # Validar si los campos no están vacíos
            if not username or not password:
                print("Campos vacíos detectados")
                QMessageBox.warning(self.window, 'Error', 'Por favor, llena ambos campos.')
                return

            print(f"Username ingresado: {username}")
            print(f"Password ingresado: {password}")

            # Validar el inicio de sesión
            if self.validate_login(username, password):
                print("Inicio de sesión exitoso")
                QMessageBox.information(self.window, 'Éxito', 'Inicio de sesión exitoso!')
                self.openCompetidor()
            else:
                print("Error en inicio de sesión")
                QMessageBox.warning(self.window, 'Error', 'Nombre de usuario o contraseña incorrectos.')

        except Exception as e:
            print(f"Error en el bloque de inicio de sesión: {e}")
            traceback.print_exc()
            QMessageBox.critical(self.window, 'Error', f'Ocurrió un error: {e}')
    
    
    def openCompetidor(self):
        print("Abriendo ventana de registro de competidores...")
        self.RegistroCompetidores = RegistroCompetidores()  # Instancia de la ventana de competidores
        self.RegistroCompetidores.show()  # Muestra la ventana
        self.window.close()  # Cierra la ventana de login
    
    
    def validate_login(self, username, password):
        connection = None
        cursor = None
        try:
            print("Intentando conectar a la base de datos...")
            connection = create_connection()  # Usar la función de conexión
            if connection is None:
                print("No se pudo establecer la conexión a la base de datos.")
                return False
        
            print("Conexión establecida, creando cursor...")
            cursor = connection.cursor()
        
            query = "SELECT password FROM usuarios WHERE username = %s"
            print(f"Ejecutando consulta: {query} con username: {username}")
            cursor.execute(query, (username,))
            result = cursor.fetchone()
        
            print(f"Resultado de la consulta: {result}")

            # Compara la contraseña ingresada con la almacenada sin cifrar
            if result and password == result[0]:
                print("La contraseña es correcta")
                return True
            else:
                print("La contraseña es incorrecta o el usuario no existe.")
                return False  # Usuario no encontrado o contraseña incorrecta

        except Error as e:
            print(f"Error al conectarse a la base de datos: {e}")
            traceback.print_exc()
            QMessageBox.critical(self.window, 'Error', f'Ocurrió un error con la base de datos: {e}')
            return False
        except Exception as e:  # Captura de errores no esperados
            print(f"Error inesperado: {e}")
            traceback.print_exc()
            QMessageBox.critical(self.window, 'Error', f'Ocurrió un error inesperado: {e}')
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = App()  # Crea una instancia de la clase App
    main_app.window.show()  # Mostrar la ventana de login
    sys.exit(app.exec_())