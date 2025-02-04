from mysql.connector import connect, Error

def create_connection():
    """Crea una conexión a la base de datos."""
    connection = None
    try:
        connection = connect(
            host='localhost',
            user='root',  # Cambia esto a tu usuario de MySQL
            password='',  # Cambia esto a tu contraseña de MySQL
            database='proyecto'  # Cambia esto al nombre de tu base de datos
        )
        print("Conexión exitosa a la base de datos")
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    return connection
