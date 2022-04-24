from paho.mqtt.client import Client
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from multiprocessing import Lock

import time
    
long = 5

def read_words(txt, long):
    lista= []
    f = open(txt, 'r')
    linea = f.readline()
    while linea != '':
        if len(linea) - 1 == long:
            lista.append(linea.strip())
        linea = f.readline()
    f.close()
    return lista
    
def elegir_palabra(txt, long):
    lista = read_words(txt, long)
    a = random.randint(0, len(lista) - 1)
    palabra = lista[a]
    return palabra

def on_connect(mqttc): #lo que tiene que hacer cuando se conecta
    mqttc.connect('clients/wordle')
"""    
def on_message(mqttc, userdata, msg): #lo que tiene que hacer cuando llegue un mensaje
    mqttc.publish(
"""
def transformar_en_codigo(palabra1, palabra2): #palabra1 y palabra2 son cadenas de caracteres.
    codigo = ''
    palabra1_ = palabra1.lower()
    palabra2_ = palabra2.lower()
    palabra1_lista = list(palabra1_)
    palabra2_lista = lista(palabra2_)
    
    for i in range(len(palabra1_lista)):
        if palabra2_lista[i] == palabra1_lista[i]:
            codigo += '2'
        elif palabra2_lista[i] != palabra1_lista[i] and palabra2_lista[i] in palabra1_lista:
            codigo += '1'
        elif not(palabra2_lista[i] in palabra1_lista):
            codigo += '0'
            
    return codigo

def anadir_intentos():
    intento = subscribe.simple(f'clients/wordle', hostname = 'wild.mat.ucm.es')
    intentos_palabras.append(intento)
    
def devolver_mensaje():
    intentos_palabras = []

    for x in intentos_palabras:
        if x == palabra:
            palabra_no_acertada = False
        else:
            if len(x) != long:
                mqttc.publish('clients/wordle', f"{x}: ERROR. La palabra debe tener 5 letras.")
            else:
                codigo = transformar_en_codigo(palabra, x)
                mqttc.publish('clients/wordle', f"{x} -> {codigo}")
        time.sleep(2)
        
def main(txt):
    mutex = Lock()
    mqttc = Client()
    
    mqttc.on_connect = on_connect
    mqttc.suscribe('clients/wordle')
    mqttc.loop_start()
    
    palabra = elegir_palabra(txt, long)    
    mqttc.publish('clients/wordle', 'Empezamos a jugar! ')
    
    palabra_no_acertada = True
    
    while palabra_no_acertada:
        mutex.acquire()
        try:
            anadir_intentos()
        finally:
            mutex.release()
        
    while palabra_no_acertada:
        mutex.acquire()
        try:
            devolver_mensaje()
        finally:
            mutex.release()
        
    mqttc.publish('clients/wordle', 'Palabra acertada!! Fin de la partida.')
    mqttc.on_disconnect()
        
if __name__ == "__main__":
    main(txt)