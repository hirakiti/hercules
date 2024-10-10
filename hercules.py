import serial.tools.list_ports
import subprocess
import os
import time

def listar_puertos_com():
    """Consulta y lista todos los puertos COM disponibles en el sistema."""
    puertos = serial.tools.list_ports.comports()

    if not puertos:
        print("No se encontraron puertos COM.")
        return None  # Devuelve None si no se encuentran puertos
    else:
        print("Puertos COM disponibles:")
        for puerto in puertos:
            print(f"Dispositivo: {puerto.device}, Descripción: {puerto.description}")
        return puertos[0].device  # Devuelve el primer puerto COM disponible

def configurar_puerto_com(puerto):
    """Configura el puerto COM con los parámetros especificados."""
    comando_mode = f"mode {puerto} baud=9600 parity=n data=8"
    try:
        # Comando mode para configurar el puerto COM
        resultado = subprocess.run(comando_mode, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"Configuración del puerto {puerto} exitosa.")
        else:
            print(f"Error al configurar el puerto {puerto}: {resultado.stderr}")
    except Exception as e:
        print(f"Excepción al configurar el puerto: {e}")

def enviar_comando(puerto, comando):
    """Envía un comando al puerto COM especificado."""
    comando_echo = f"echo {comando} > {puerto}"
    try:
        # Comando echo para enviar el comando al puerto COM
        resultado = subprocess.run(comando_echo, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"Comando '{comando}' enviado exitosamente al puerto {puerto}.")
        else:
            print(f"Error al enviar el comando '{comando}': {resultado.stderr}")
    except Exception as e:
        print(f"Excepción al enviar el comando: {e}")

if __name__ == "__main__":
    # Obtiene el puerto COM automáticamente
    puerto_com = listar_puertos_com()  # Llama a la función para listar los puertos y guarda el primero
    
    if puerto_com:
        configurar_puerto_com(puerto_com)
        
        comandos = [
            '@FACTORY_RESET',
            '@REBOOT',
            '@GET_FIRMWARE_VERSION',
            '@SET_PRIORITY:1>0>2>3',
            '@REBOOT'
        ]
        
        for comando in comandos:
            enviar_comando(puerto_com, comando)
            time.sleep(5)  # Espera de 5 segundos entre cada comando

    else:
        print("No se encontró ningún puerto COM disponible.")
