import serial.tools.list_ports
import subprocess
import os
import time
import pyautogui

def listar_puertos_com():
    """Consulta y lista todos los puertos COM disponibles en el sistema."""
    puertos = serial.tools.list_ports.comports()
    
    if not puertos:
        print("No se encontraron puertos COM.")
    else:
        print("Puertos COM disponibles:")
        for puerto in puertos:
            print(f"Dispositivo: {puerto.device}, Descripción: {puerto.description}")

def ejecutar_programa():
    """Ejecuta el programa hercules_3-2-8.exe desde la ubicación especificada."""
    ruta_programa = r"C:\hercules_3-2-8.exe"  # Ruta completa al programa
    if os.path.exists(ruta_programa):
        try:
            # Abre una nueva ventana de CMD y ejecuta el programa
            cmd_command = f'start cmd /K "{ruta_programa}"'
            subprocess.Popen(cmd_command, shell=True)
            print(f"Ejecutando {ruta_programa} en una nueva terminal...")
            time.sleep(3)  # Espera para que el programa se abra
            
            # Cambia a la pestaña Serial (ajusta las coordenadas)
            pyautogui.click(100, 100)  # Cambia estas coordenadas a las de la pestaña Serial
            time.sleep(1)  # Espera un segundo
            
            # Enviar comandos
            comandos = [
                '##FACTORY_RESET\r\n',
                '##REBOOT\r\n',
                '##GET_FIRMWARE_VERSION\r\n',
                '##SET_PRIORITY:1>0>2>3\r\n',
                '##REBOOT\r\n'
            ]
            
            for comando in comandos:
                pyautogui.typewrite(comando)  # Escribe el comando en el campo de texto
                time.sleep(0.5)  # Espera medio segundo
                pyautogui.press('enter')  # Presiona Enter para enviar el comando
                time.sleep(1)  # Espera un segundo entre comandos
            
            print("Comandos enviados.")
        except Exception as e:
            print(f"No se pudo ejecutar el programa: {e}")
    else:
        print(f"El programa no se encuentra en la ruta especificada: {ruta_programa}")

if __name__ == "__main__":
    listar_puertos_com()   # Llama a la función para listar los puertos
    ejecutar_programa()    # Llama a la función para ejecutar el programa
    input("Presiona Enter para salir...")  # Pausa antes de cerrar
