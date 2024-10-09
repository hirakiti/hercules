import serial.tools.list_ports
import serial
import time

def listar_puertos_com():
    """Lista todos los puertos COM disponibles y retorna el primero."""
    puertos = serial.tools.list_ports.comports()
    
    if not puertos:
        print("No se encontraron puertos COM.")
        return None
    else:
        print("Puertos COM disponibles:")
        for puerto in puertos:
            print(f"Dispositivo: {puerto.device}, Descripción: {puerto.description}")
        return puertos[0].device  # Devuelve el primer puerto COM disponible

def abrir_puerto_com(puerto):
    """Abre el puerto COM especificado con la configuración adecuada."""
    try:
        ser = serial.Serial(puerto, baudrate=9600, timeout=1)
        print(f"Puerto {puerto} abierto correctamente.")
        return ser
    except Exception as e:
        print(f"Error al abrir el puerto {puerto}: {e}")
        return None

def enviar_comando(ser, comando):
    """Envía un comando al puerto serie."""
    try:
        ser.write(comando.encode())  # Envía el comando codificado en bytes
        time.sleep(0.5)  # Espera un momento para asegurarse de que el comando se procese
        print(f"Comando enviado: {comando.strip()}")
        
        # Leer la respuesta del dispositivo
        respuesta = ser.read_all().decode('utf-8', errors='ignore')
        if respuesta:
            print(f"Respuesta recibida: {respuesta}")
        else:
            print("No se recibió respuesta.")
    except Exception as e:
        print(f"Error al enviar el comando: {e}")

def cerrar_puerto_com(ser):
    """Cierra el puerto serie."""
    if ser:
        ser.close()
        print("Puerto cerrado.")

if __name__ == "__main__":
    # Listar puertos COM y seleccionar el primero
    puerto_com = listar_puertos_com()
    
    if puerto_com:
        # Abrir el puerto COM
        ser = abrir_puerto_com(puerto_com)
        
        if ser:
            # Comandos a enviar
            comandos = [
                '##FACTORY_RESET\r\n',
                '##REBOOT\r\n',
                '##GET_FIRMWARE_VERSION\r\n',
                '##SET_PRIORITY:1>0>2>3\r\n',
                '##REBOOT\r\n'
            ]

            # Enviar cada comando
            for comando in comandos:
                enviar_comando(ser, comando)
                time.sleep(2)  # Pausa entre comandos para dar tiempo al dispositivo a procesarlos
            
            # Cerrar el puerto COM
            cerrar_puerto_com(ser)

        else:
            print("No se pudo abrir el puerto COM.")
    else:
        print("No se encontró ningún puerto COM.")
