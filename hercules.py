import serial.tools.list_ports
import subprocess
import os
import time
import pyautogui
import pygetwindow as gw

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

def ejecutar_programa():
    """Ejecuta el programa hercules_3-2-8.exe desde la ubicación especificada."""
    ruta_programa = r"C:\hercules_3-2-8.exe"  # Ruta completa al programa
    
    if os.path.exists(ruta_programa):
        try:
            # Ejecuta el programa y mantiene la ventana de comandos abierta
            print(f"Ejecutando {ruta_programa}...")
            subprocess.run([ruta_programa], shell=True)  # Usa run() para ejecutar y mostrar la salida en la consola
            time.sleep(5)  # Espera de unos segundos para que el programa se inicie completamente
        except Exception as e:
            print(f"No se pudo ejecutar el programa: {e}")
    else:
        print(f"El programa no se encuentra en la ruta especificada: {ruta_programa}")

def enfocar_ventana(nombre_programa):
    """Enfoca la ventana del programa especificado usando pygetwindow."""
    windows = gw.getWindowsWithTitle(nombre_programa)
    if windows:
        ventana = windows[0]  # Toma la primera coincidencia
        ventana.activate()  # Activa la ventana
        print(f"Ventana '{nombre_programa}' activada.")
        time.sleep(1)  # Da tiempo para que la ventana se enfoque
    else:
        print(f"No se encontró ninguna ventana con el nombre '{nombre_programa}'.")

def navegar_a_serial():
    """Navega a la pestaña 'Serial' en el programa Hercules usando pyautogui."""    
    enfocar_ventana("Hercules")  # Asegura que la ventana esté en foco antes de enviar comandos
    time.sleep(2)  # Espera unos segundos antes de empezar a enviar comandos de navegación

    # Simula las teclas 'Tab' para moverse por la interfaz
    for _ in range(12):
        pyautogui.press('tab')
        time.sleep(0.2)  # Pausa breve entre cada Tab para asegurarse de que el programa registre las teclas

    # Usa la flecha derecha para seleccionar la pestaña "Serial"
    pyautogui.press('right')
    print("Navegando a la pestaña 'Serial'...")

def seleccionar_puerto_com():
    """Selecciona automáticamente el primer puerto COM disponible."""
    puerto = listar_puertos_com()  # Obtiene el primer puerto COM
    if puerto:  # Verifica si hay un puerto disponible
        print(f"Seleccionando el puerto: {puerto}")
        time.sleep(1)  # Espera un momento
        pyautogui.press('tab')  # Tabula para enfocarse en la lista de puertos COM
        time.sleep(0.5)  # Pausa para asegurarse de que se registre la acción
        pyautogui.typewrite(puerto)  # Escribe el puerto COM
        pyautogui.press('enter')  # Presiona enter para seleccionarlo
        time.sleep(1)  # Espera un segundo para que se procese la selección
    else:
        print("No hay puertos COM disponibles para seleccionar.")

def enviar_comandos():
    """Envía comandos específicos al puerto 'Serial'."""
    # Definición de los comandos a enviar
    comandos = [
        '##FACTORY_RESET\r\n',               # 1 comando
        '##REBOOT\r\n',                      # 2 comando
        '##GET_FIRMWARE_VERSION\r\n',       # 3 comando
        '##SET_PRIORITY:1>0>2>3\r\n',       # 4 comando
        '##REBOOT\r\n'                      # 5 comando
    ]

    # Enviar el primer comando
    print("Enviando comando: ##FACTORY_RESET")
    for _ in range(6):  # 6 tabulaciones
        pyautogui.press('tab')  
    pyautogui.typewrite(comandos[0])  # Escribe el primer comando
    pyautogui.press('enter')  # Presiona enter
    time.sleep(2)  # Aumenta el tiempo de espera después de enviar el primer comando

    # Enviar los siguientes comandos
    for i in range(1, len(comandos)):
        print(f"Enviando comando: {comandos[i].strip()}")
        for _ in range(8):  # 8 tabulaciones
            pyautogui.press('tab')  
        pyautogui.typewrite(comandos[i])  # Escribe el comando actual
        for _ in range(6):  # 6 tabulaciones
            pyautogui.press('tab')  
        pyautogui.press('enter')  # Presiona enter
        time.sleep(2)  # Aumenta el tiempo de espera después del comando

    print("Todos los comandos han sido enviados correctamente.")

if __name__ == "__main__":
    ejecutar_programa()    # Llama a la función para ejecutar el programa
    time.sleep(3)          
    navegar_a_serial()     # Navega a la pestaña Serial
    seleccionar_puerto_com()  # Selecciona el primer puerto COM disponible
    enviar_comandos()      # Envía los comandos
    input("Presiona Enter para salir...")  # Pausa antes de cerrar
