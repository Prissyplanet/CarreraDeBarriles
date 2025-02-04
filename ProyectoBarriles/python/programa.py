import serial

puerto = 'COM5'
baud_rate = 4800  # Cambia este valor si la máquina usa otro baud rate

try:
    with serial.Serial(puerto, baud_rate, timeout=1) as ser:
        print(f"Conectado al puerto {puerto}. Leyendo datos...")
        while True:
            # Lee una línea de datos del puerto serial
            linea = ser.readline().decode('utf-8').strip()
            if linea:
                print(f"Dato recibido: {linea}")
except serial.SerialException as e:
    print(f"No se pudo abrir el puerto: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
