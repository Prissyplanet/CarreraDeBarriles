#!/usr/bin/env python3
# -- coding: utf-8 --

import sys, time, re
from datetime import datetime

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Instala pyserial: pip install pyserial")
    sys.exit(1)

PORT = "COM3"       # cámbialo si usas otro
BAUD = 9600
TIMEOUT = 0.05      # lectura “rápida” para no perder ráfagas

# Regex de tiempos comunes de cronometraje: 12.345  |  1:02.345  |  00:01:02.345
PAT_TIME = re.compile(
    r"(?:\b\d{1,2}:\d{2}:\d{2}\.\d{1,3}\b|\b\d{1,2}:\d{2}\.\d{1,3}\b|\b\d{1,3}\.\d{1,3}\b)"
)

def hexdump(b: bytes) -> str:
    return b.hex()

def as_ascii(b: bytes) -> str:
    try:
        return b.decode("ascii", errors="replace")
    except Exception:
        return repr(b)

def open_ser(port, baud):
    ser = serial.Serial(
        port=port,
        baudrate=baud,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=TIMEOUT,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    )
    # Muchos dispositivos “despiertan” con DTR/RTS altos
    try:
        ser.dtr = True
        ser.rts = True
    except Exception:
        pass
    return ser

def print_line(kind: str, data: bytes):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] {kind:<6} HEX:{hexdump(data)}  TXT:{as_ascii(data)}")

def main():
    # Ayuda visual de puertos
    ports = list(serial.tools.list_ports.comports())
    print("Puertos detectados:")
    for i, p in enumerate(ports, 1):
        print(f" [{i}] {p.device} - {p.description}")
    chosen = input(f"Puerto a usar [default: {PORT}]: ").strip() or PORT

    last_time_str = None
    buf = b""

    try:
        with open_ser(chosen, BAUD) as ser:
            print(f"\nEscuchando Scoreboard en {ser.port} @ {ser.baudrate} (8N1).")
            print("Acción: pon el Polaris en Scoreboard Type → ASCII → 4800, haz un run con Eyes.\n")
            print("Imprimo CHUNKs crudos, LINE (por CR/LF) y FRAME (por STX/ETX). Si veo un tiempo, lo marco como TIME.\n")

            while True:
                try:
                    chunk = ser.read(ser.in_waiting or 1)
                    if chunk:
                        buf += chunk
                        print_line("CHUNK", chunk)

                        # 1) Frames por STX..ETX (0x02..0x03)
                        while True:
                            stx = buf.find(b"\x02")
                            etx = buf.find(b"\x03", stx + 1) if stx != -1 else -1
                            if stx != -1 and etx != -1:
                                frame = buf[stx+1:etx]
                                print_line("FRAME", frame)
                                # busca tiempos dentro del frame
                                txt = as_ascii(frame)
                                m = PAT_TIME.search(txt)
                                if m:
                                    tval = m.group(0)
                                    if tval != last_time_str:
                                        last_time_str = tval
                                        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                                        print(f"[{ts}] TIME   {tval}")
                                # descarta lo consumido
                                buf = buf[etx+1:]
                                continue
                            break

                        # 2) Líneas por CR/LF
                        while True:
                            # separa por el primer CR o LF que aparezca
                            pos_cr = buf.find(b"\r")
                            pos_lf = buf.find(b"\n")
                            cuts = [p for p in (pos_cr, pos_lf) if p != -1]
                            if not cuts:
                                break
                            cut = min(cuts)
                            line, buf = buf[:cut], buf[cut+1:]
                            print_line("LINE ", line)
                            txt = as_ascii(line)
                            m = PAT_TIME.search(txt)
                            if m:
                                tval = m.group(0)
                                if tval != last_time_str:
                                    last_time_str = tval
                                    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                                    print(f"[{ts}] TIME   {tval}")

                except KeyboardInterrupt:
                    print("\nDetenido por el usuario.")
                    if buf:
                        print_line("REMAIN", buf)
                    break

    except serial.SerialException as e:
        print(f"No se pudo abrir {chosen} @ {BAUD}: {e}")

if __name__ == "__main__":
    main()