import serial
import time

puerto = 'COM8'
velocidad_baudios = 4800

try:
    # Abre el puerto serial
    ser = serial.Serial(puerto, velocidad_baudios, timeout=1)
    print(f"Conectado a {puerto} a {velocidad_baudios} baudios")
    time.sleep(2)  # Espera para asegurar que el puerto esté listo

    # Revisa continuamente si hay datos en el puerto
    while True:
        if ser.in_waiting > 0:  # Si hay datos en el buffer de entrada
            datos = ser.read(ser.in_waiting)  # Lee los datos recibidos
            print("Datos recibidos:", datos)
        else:
            print("Esperando datos de la máquina...")

except serial.SerialException as e:
    print(f"Error al abrir el puerto: {e}")
except KeyboardInterrupt:
    print("\nConexión finalizada por el usuario.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
