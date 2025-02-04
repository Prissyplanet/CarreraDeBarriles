from db_connection import create_connection
from PyQt5.QtWidgets import QMessageBox

def registrar_competidor(nombre, caballo, lugar, categoria, division, afiliado):
    # Verificar si todos los campos están completos
    if not nombre or not caballo or not lugar or not categoria or not division or not afiliado:
        QMessageBox.critical(None, "Error", "Por favor, complete todos los campos antes de registrar.")
        return
    
    # Conectar a la base de datos
    connection = create_connection()
    if not connection:
        QMessageBox.critical(None, "Error de conexión", "No se pudo conectar a la base de datos.")
        return
    
    try:
        # Preparar la consulta para insertar los datos
        cursor = connection.cursor()
        query = """
            INSERT INTO ronda_larga (nombre, caballo, lugar, categoria, division, afiliado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (nombre, caballo, lugar, categoria, division, afiliado)
        cursor.execute(query, values)
        connection.commit()

        # Mostrar mensaje de éxito
        QMessageBox.information(None, "Éxito", "Competidor registrado correctamente.")
        
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

    except Exception as e:
        # Manejar posibles errores en la inserción
        QMessageBox.critical(None, "Error", f"Se produjo un error al registrar el competidor: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
