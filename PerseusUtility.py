import serial
import serial.tools.list_ports
import time

# Detecta los puertos serie disponibles que tengan como nombre "USB Serial Port"
def encontrar_puerto_serial():
    puertos = list(serial.tools.list_ports.comports())
    if len(puertos) == 0:
        print("No hay puertos seriales disponibles.")
        return None
    else:
        for puerto in puertos:
            if "USB Serial Port" in puerto.description:  # Busca si el puerto es "USB Serial Port"
                print(f"Puerto USB Serial Port encontrado: {puerto.device}")
                return puerto.device
        print("No se encontró un puerto con el nombre 'USB Serial Port'.")
        return None

# Envia los comandos y verifica su respuesta
def enviar_comando_y_verificar(ser, comando, descripcion, log_file):
    ser.reset_input_buffer()  # Limpia el buffer de entrada
    ser.write(comando.encode())  
    print(f"{descripcion}: {comando.strip()}")
    time.sleep(2)  # Espera 2 segundos para dar tiempo a procesar

    respuesta = ""
    # Lee hasta que no haya más datos disponibles
    start_time = time.time()  # Registra el tiempo de inicio
    while time.time() - start_time < 5:  # Espera hasta 5 segundos
        if ser.inWaiting() > 0:  
            respuesta += ser.readline().decode('utf-8', errors='ignore').strip() + "\n"
        time.sleep(0.1)  

    # Registra la respuesta en el archivo de log
    log_file.write(f"{descripcion}: {respuesta.strip()}\n")

    if respuesta:
        print(f"{descripcion}: {respuesta.strip()}")
    else:
        print(f"{descripcion}: No se recibió respuesta del dispositivo.")

# Función principal
def gestionar_puerto_serial():
    puerto = encontrar_puerto_serial()
    if not puerto:
        return
    
    try:
        # Configura la conexión serie con las siguientes especificaciones 
        ser = serial.Serial(
            port=puerto,             # Puerto encontrado
            baudrate=9600,           # Velocidad de transmisión: 9600 bps
            bytesize=serial.EIGHTBITS,  # Tamaño de los datos: 8 bits
            parity=serial.PARITY_NONE,  # Paridad: ninguna
            stopbits=serial.STOPBITS_ONE,  # 1 bit de stop
            xonxoff=False,           # Control de flujo por software: deshabilitado
            rtscts=False,            # Control de flujo por hardware (RTS/CTS): deshabilitado
            dsrdtr=False,            # DSR/DTR: deshabilitado (handshake desactivado)
            timeout=3                # Timeout de 3 segundos para las lecturas
        )
        print(f"Puerto {puerto} abierto con configuración: baudrate=9600, paridad=None, handshake=off, modo=free.")
        
        # Abre el archivo de log
        with open("registro_comandos.txt", "w") as log_file:
            # Comando 1: FACTORY RESET
            enviar_comando_y_verificar(ser, "#FACTORY_RESET\r\n", "Factory Reset ejecutado", log_file)
            time.sleep(10)  # Espera 10 segundos para que el dispositivo reinicie

            # Comando 2: Obtener versión del firmware
            enviar_comando_y_verificar(ser, "#GET_FIRMWARE_VERSION\r\n", "Versión del firmware", log_file)
            time.sleep(2)  # Espera 2 segundos después de obtener la versión

            # Comando 3: Configurar el orden de prioridad
            enviar_comando_y_verificar(ser, "#SET_PRIORITY:1>0>2>3\r\n", "Orden de prioridad enviada", log_file)
            time.sleep(2)  # Espera 2 segundos después de enviar la orden de prioridad

            # Comando 4: Reiniciar el dispositivo
            enviar_comando_y_verificar(ser, "#REBOOT\r\n", "Reinicio ejecutado", log_file)
            time.sleep(5)  # Espera 5 segundos para que el dispositivo reinicie de nuevo

        # Cerrar puerto
        ser.close()
        print(f"Puerto {puerto} cerrado.")

    except serial.SerialException as e:
        print(f"Error al abrir el puerto: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    gestionar_puerto_serial()

