from paho.mqtt.client import Client
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import sys
import time

def on_connect(mqttc):
    mqttc.connect('wild.mat.ucm.es')
    mqttc.subscribe('clients/wordle')
    nombre = input('Vamos a jugar al wordle. El objetivo es adivinar la palabra de 5 letras que estoy pensando. Para ello, tendrás que ir lanzándome palabras de 5 letras. Yo te devolveré una serie de 5 numeros según las letras de la palabra que has elegido están en mi palabra o no. Si pongo un 0, la letra no está en mi palabra; si pongo un 1 la letra está en la palbra pero en otra posición; y si pongo un 2 la letra está en la palabra y además ocupa la misma posición que en tu palabra. "¿Cual es tu nombre? ')
    return nombre
    
def on_publish(mqttc, nombre):
    palabra_jugador = input(f'{nombre}, prueba otra palabra: ')
    mqqtc.publish('clients/wordle', f'{nombre} ha probado la palabra: {palabra_jugador}')
    
    
def main():
    mqttc = Client()
    
    mqttc.on_connect = on_connect
    nombre = on_connect(mqttc)
    mqttc.loop_start()
    
    while True:
        mqttc.on_publish = on_publish(mqttc, nombre)
        time.sleep(2)

    mqttc.loop_stop()
    mqttc.disconnect()
    

if __name__ == '__main__':
    main()