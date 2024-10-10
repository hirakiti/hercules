import serial.tools.list_ports
import subprocess
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

def configurar_puerto_sistema(puerto):
    """Configura el puerto COM en el sistema usando el comando mode."""
    try:
        # Comando mode en función del puerto COM detectado
        comando = f"mode {puerto} baud=9600 parity=n data=8"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"Configuración del puerto {puerto} exitosa.")
        else:
            print(f"Error al configurar el puerto {puerto}: {resultado.stderr}")
    except Exception as e:
        print(f"Error al ejecutar el comando mode: {e}")

def enviar_comando_echo(puerto, comando):
    """Envía el comando echo al puerto COM."""
    try:
        comando_echo = f'echo {comando.strip()} > {puerto}'
        resultado = subprocess.run(comando_echo, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"Comando '{comando.strip()}' enviado exitosamente al puerto {puerto}.")
        else:
            print(f"Error al enviar el comando '{comando.strip()}': {resultado.stderr}")
    except Exception as e:
        print(f"Error al ejecutar el comando echo: {e}")

if __name__ == "__main__":
    # Listar puertos COM y seleccionar el primero
    puerto_com = listar_puertos_com()
    
    if puerto_com:
        # Configurar el puerto en el sistema con el comando mode
        configurar_puerto_sistema(puerto_com)

        # Comandos a enviar con terminaciones \r\n
        comandos = [
            '##FACTORY_RESET\r\n',
            '##REBOOT\r\n',
            '##GET_FIRMWARE_VERSION\r\n',
            '##SET_PRIORITY:1>0>2>3\r\n',
            '##REBOOT\r\n'
        ]

        for comando in comandos:
            enviar_comando_echo(puerto_com, comando)
            time.sleep(2)  # Espera de 2 segundos entre comandos

    else:
        print("No se encontró ningún puerto COM.")
