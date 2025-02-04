from db_connection import create_connection
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt


from db_connection import create_connection
from PyQt5.QtWidgets import QMessageBox

def actualizar_competidores_por_categoria(categoria_seleccionada, combobox_competidor):
    """
    Actualiza el combobox de competidores con los registrados en la categoría seleccionada.
    
    :param categoria_seleccionada: Categoría seleccionada en el combobox de categoría.
    :param combobox_competidor: Referencia al combobox de competidores.
    """
    if categoria_seleccionada == "Selecciona una categoría":
        combobox_competidor.clear()
        combobox_competidor.addItem("Selecciona un competidor")
        return

    connection = create_connection()
    if not connection:
        QMessageBox.critical(None, "Error de conexión", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        query = """
            SELECT nombre, caballo FROM ronda_larga
            WHERE categoria = %s
        """
        cursor.execute(query, (categoria_seleccionada,))
        competidores = cursor.fetchall()
        connection.close()

        # Limpiar y actualizar el combobox de competidores
        combobox_competidor.clear()
        combobox_competidor.addItem("Selecciona un competidor")
        for competidor in competidores:
            competidor_texto = f"{competidor[0]} - {competidor[1]}"
            combobox_competidor.addItem(competidor_texto)

    except Exception as e:
        QMessageBox.critical(None, "Error en la consulta", f"Error al cargar los competidores: {e}")


from db_connection import create_connection
from PyQt5.QtWidgets import QMessageBox


from db_connection import create_connection
from PyQt5.QtWidgets import QMessageBox

def cargar_competidores(combobox_competidor, categoria_seleccionada=None):
    """
    Carga los competidores registrados en la base de datos.
    """
    if not categoria_seleccionada or categoria_seleccionada == "Selecciona una categoría":
        combobox_competidor.clear()
        combobox_competidor.addItem("Selecciona un competidor")
        combobox_competidor.setEnabled(False)
        return

    connection = create_connection()
    if not connection:
        QMessageBox.critical(None, "Error de conexión", "No se pudo conectar a la base de datos.")
        combobox_competidor.setEnabled(False)
        return

    try:
        cursor = connection.cursor()
        query = "SELECT nombre, caballo FROM ronda_larga WHERE categoria = %s"
        cursor.execute(query, (categoria_seleccionada,))
        competidores = cursor.fetchall()

        combobox_competidor.clear()
        combobox_competidor.addItem("Selecciona un competidor")
        for competidor in competidores:
            nombre_completo = f"{competidor[0]} ({competidor[1]})"
            combobox_competidor.addItem(nombre_completo)

        combobox_competidor.setEnabled(True)  # Habilitar después de cargar

    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error al cargar los competidores: {e}")
        combobox_competidor.setEnabled(False)
    finally:
        if connection:
            connection.close()


def cargar_tabla_por_categoria(categoria_seleccionada, tabla):
    """
    Filtra los datos de la base de datos según la categoría seleccionada
    y los muestra en la tabla de la interfaz.
    """
    if not categoria_seleccionada or categoria_seleccionada == "Selecciona una categoría":
        tabla.setRowCount(0)  # Limpiar la tabla si no se selecciona una categoría válida
        return

    connection = create_connection()
    if not connection:
        QMessageBox.critical(None, "Error de conexión", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        query = """
            SELECT nombre, caballo, lugar, tiempo, puesto, puntos, categoria, division, afiliado
            FROM ronda_larga
            WHERE categoria = %s
        """
        cursor.execute(query, (categoria_seleccionada,))
        resultados = cursor.fetchall()

        # Limpiar la tabla
        tabla.setRowCount(0)

        # Poblar la tabla con los resultados obtenidos
        for fila, registro in enumerate(resultados):
            tabla.insertRow(fila)
            for columna, valor in enumerate(registro[:-1]):
                if columna == 5 and registro[-1] == "NO AFILIADO":
                    item = QTableWidgetItem("NO AFILIADO")
                else:
                    item = QTableWidgetItem(str(valor) if valor is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                tabla.setItem(fila, columna, item)

        cursor.close()
        connection.close()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error al cargar los datos de la tabla: {e}")
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def verificar_afiliacion(competidor_seleccionado, puntos_input):
    """
    Verifica si el competidor seleccionado está afiliado y ajusta el campo de puntos en consecuencia.
    """
    if not competidor_seleccionado or competidor_seleccionado == "Selecciona un competidor":
        puntos_input.setEnabled(False)
        puntos_input.setText("")
        return

    nombre_competidor = competidor_seleccionado.split(" (")[0]

    connection = create_connection()
    if not connection:
        QMessageBox.critical(None, "Error de conexión", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        query = "SELECT afiliado FROM ronda_larga WHERE nombre = %s"
        cursor.execute(query, (nombre_competidor,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()

        if resultado and resultado[0] == "NO AFILIADO":
            puntos_input.setEnabled(False)
            puntos_input.setText("NO AFILIADO")
        else:
            puntos_input.setEnabled(True)
            puntos_input.setText("")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error al verificar la afiliación: {e}")

def registrar_valores(competidor_seleccionado, tiempo, puntos):
    """
    Registra el tiempo y puntos para el competidor en la base de datos.

    :param competidor_seleccionado: Competidor seleccionado en el formato "Nombre (Caballo)".
    :param tiempo: Tiempo registrado.
    :param puntos: Puntos registrados (opcional).
    :return: True si la operación fue exitosa, False en caso contrario.
    """
    # Extraer solo el nombre del competidor
    nombre_competidor = competidor_seleccionado.split(" (")[0]

    connection = create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        # Actualizar los valores en la base de datos
        query = "UPDATE ronda_larga SET tiempo = %s, puntos = %s WHERE nombre = %s"
        cursor.execute(query, (tiempo, puntos or None, nombre_competidor))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al registrar los valores: {e}")
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return False
def recalcular_puestos(categoria):
    """
    Recalcula los puestos de los competidores en una categoría específica
    basado en sus tiempos registrados.

    :param categoria: Categoría para la que se calcularán los puestos.
    """
    connection = create_connection()
    if not connection:
        print("No se pudo conectar a la base de datos para recalcular los puestos.")
        return

    try:
        cursor = connection.cursor()
        # Obtener competidores de la categoría con sus tiempos
        query = """
            SELECT id, tiempo
            FROM ronda_larga
            WHERE categoria = %s AND tiempo IS NOT NULL
            ORDER BY tiempo ASC
        """
        cursor.execute(query, (categoria,))
        competidores = cursor.fetchall()

        # Recalcular puestos
        for puesto, (id_competidor, _) in enumerate(competidores, start=1):
            update_query = "UPDATE ronda_larga SET puesto = %s WHERE id = %s"
            cursor.execute(update_query, (puesto, id_competidor))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Puestos recalculados para la categoría {categoria}.")
    except Exception as e:
        print(f"Error al recalcular puestos: {e}")
        if cursor:
            cursor.close()
        if connection:
            connection.close()
