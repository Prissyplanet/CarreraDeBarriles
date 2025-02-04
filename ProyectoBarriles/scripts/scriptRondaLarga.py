from db_connection import create_connection

def registrar_competidor(nombre, caballo, lugar, tiempo, puntos, categoria, division):
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
            puesto_campeon = i + 1  # El puesto es el índice + 1 (1 para el mejor tiempo, 2 para el segundo, etc.)

            # Actualizar el puesto del campeón en la base de datos
            query_update = """UPDATE ronda_larga SET campeon = %s WHERE id = %s"""
            cursor.execute(query_update, (puesto_campeon, competidor_id))

        connection.commit()

    except Exception as e:
        print(f"Error al registrar el competidor: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def actualizar_tabla():
    # Crear conexión con la base de datos
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        query = """SELECT nombre, caballo, lugar, tiempo, campeon, puntos, categoria, division FROM ronda_larga"""
        cursor.execute(query)
        competidores = cursor.fetchall()

        return competidores

    except Exception as e:
        print(f"Error al actualizar la tabla: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def asignar_campeones(categoria, division):
    # Conectar a la base de datos
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()

        # Obtener los competidores de la categoría y división, ordenados por tiempo
        query_select = """SELECT id, nombre, tiempo FROM ronda_larga
                          WHERE categoria = %s AND division = %s ORDER BY tiempo ASC"""
        cursor.execute(query_select, (categoria, division))
        competidores = cursor.fetchall()

        # Asignar campeones (posición por tiempo)
        for index, competidor in enumerate(competidores):
            competidor_id = competidor[0]
            campeon_pos = index + 1  # El primer lugar tiene el mejor tiempo

            # Actualizar la posición del campeón en la base de datos
            query_update = """UPDATE ronda_larga SET campeon = %s WHERE id = %s"""
            cursor.execute(query_update, (campeon_pos, competidor_id))

        connection.commit()
        print("Campeones asignados correctamente.")

    except Exception as e:
        print(f"Error al asignar campeones: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def validar_divisiones(categoria, competidores):
    """
    Validar las divisiones y asignar las divisiones de acuerdo a la categoría.
    """
    if categoria == 'Abierta':
        divisiones = ['Primera', 'Segunda', 'Tercera', 'Cuarta', 'Quinta', 'Sexta']
        divisiones_lugares = 6  # 6 lugares para campeones en cada división
    elif categoria == 'Juvenil':
        divisiones = ['Primera', 'Segunda', 'Tercera']
        divisiones_lugares = 2  # 2 lugares para campeones en cada división
    elif categoria == 'Infantil':
        divisiones = ['General']
        divisiones_lugares = 3  # 3 lugares para campeones, sin divisiones
    else:
        print("Categoría no válida.")
        return

    # Asignación de divisiones a competidores
    competidores_divididos = {division: [] for division in divisiones}

    # Asignar a los competidores a las divisiones
    for i, competidor in enumerate(competidores):
        division = divisiones[i % len(divisiones)]  # Distribuir los competidores entre las divisiones
        competidores_divididos[division].append(competidor)

    # Asignar los campeones por división
    for division, competidores_in_division in competidores_divididos.items():
        competidores_in_division.sort(key=lambda x: x[1])  # Ordenar por tiempo
        for index, competidor in enumerate(competidores_in_division[:divisiones_lugares]):
            competidor_id = competidor[0]
            campeon_pos = index + 1
            connection = create_connection()
            if connection is None:
                print("No se pudo conectar a la base de datos.")
                return
            cursor = connection.cursor()

            query_update = """UPDATE ronda_larga SET campeon = %s, division = %s WHERE id = %s"""
            cursor.execute(query_update, (campeon_pos, division, competidor_id))
            connection.commit()

    print(f"Divisiones y campeones asignados para la categoría {categoria}.")