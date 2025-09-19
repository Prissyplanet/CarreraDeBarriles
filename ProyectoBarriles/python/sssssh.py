import serial
from datetime import datetime

PORT = "COM3"
BAUD = 9600

with serial.Serial(PORT, BAUD, timeout=0.05) as ser, \
     open("polaris_capture.bin", "ab") as fbin, \
     open("polaris_capture.txt", "a", encoding="utf-8") as ftxt:

    print(f"Escuchando {PORT} @ {BAUD}. Haz un run y luego Ctrl+C para parar.\n")

    try:
        while True:
            data = ser.read(ser.in_waiting or 1)
            if data:
                fbin.write(data)
                fbin.flush()
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                hex_str = " ".join(f"{b:02X}" for b in data)
                print(f"[{ts}] {hex_str}")
                ftxt.write(f"[{ts}] {hex_str}\n")
                ftxt.flush()
    except KeyboardInterrupt:
        print("\nCaptura detenida. Archivos guardados:")
        print(" - polaris_capture.bin")
        print(" - polaris_capture.txt")