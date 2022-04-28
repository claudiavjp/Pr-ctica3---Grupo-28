from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep
import pygame
from pygame.locals import *
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

public_topic = 'clients/cvinas/wordle'

pygame.init()
ventana = pygame.display.set_mode((400,300))
pygame.display.set_caption("Wordle")
fuente = pygame.font.Font(None, 30)

def on_message(mqttc, userdata, msg):
    #print('on_message', msg.topic, msg.payload)
    i = 0
    if msg.topic == public_topic: #REALMENTE POR EL CANAL PRIVADO EL CLIENTE NO VA A RECIBIR NINGÃN MENSAJE
        mensaje = msg.payload.decode('utf-8')
        if mensaje[0] == 'N':
            texto = fuente.render(f'{mensaje[1:]} se ha unido a la partida', 0, (200,60,80))
            ventana.blit(texto, (0 + i,0))
            i += 1
        else:
            texto = fuente.render(mensaje , 0, (200,60,80))
            ventana.blit(texto, (0 + i,0))
            print(mensaje)
            i += 1
    pygame.display.update()
    #worker = Process(target = work_on_message, args = (str(msg.payload), userdata['broker']))
    #worker.start()
    #print('end on_message', msg.payload)
    
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def get_name():
    name = input("dame tu alias: ")
    return name

def main(broker):
    userdata = {
        'broker': broker,
        'mychannel': '',
    }
    
    mqttc = Client(userdata = userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message
    #mqttc.on_log = on_log
    mqttc.connect(broker)

    mqttc.subscribe(public_topic)
    myname = get_name()

    userdata['mychannel'] = f'{public_topic}/{myname}'
    mqttc.subscribe(userdata['mychannel'])
    mqttc.publish(public_topic, f'N{myname}')

    mqttc.loop_start()
    while True:
        word = input('dame una palabra: ')
        mqttc.publish(userdata['mychannel'], f'W{word}')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
