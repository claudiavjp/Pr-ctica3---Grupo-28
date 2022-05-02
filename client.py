########################################################################################
########################################################################################
###############                                                          ###############
###############            PRÁCTICA 3 - PROGRAMACIÓN PARALELA            ###############
###############                   Cristina Ávila Santos                  ###############
###############                   Isabel Beltrá Merino                   ###############
###############                   Claudia Viñas JÃ¡Ã±ez                  ###############
###############                                                          ###############
########################################################################################
########################################################################################

from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep

public_topic = 'clients/cvinas/wordle'

def on_message(mqttc, userdata, msg):
    if msg.topic == public_topic:
        mensaje = msg.payload.decode('utf-8')
        if mensaje[0] == 'N':
            print(f'{mensaje[1:]} se ha unido a la partida')
        elif mensaje[0] == 'M':
            print(mensaje[1:])
        else:
            pass
    else:
        pass

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def get_name():
    print('Vamos a jugar al WORDLE. \n El objetivo es adivinar la palabra de 5 letras que estoy pensando. Para ello, tendrás que ir lanzándome palabras de 5 letras. Yo te devolveré una serie de 5 numeros en función de si las letras de la palabra que has elegido están en mi palabra o no. \n - Si pongo un 2, la letra NO está en mi palabra. \n - Si pongo un 1 la letra está en la palbra pero en otra posición. \n - Si pongo un 0 la letra está en la palabra y además ocupa la misma posición que en tu palabra.\n ¡A JUGAR!')
    name = input("Dame tu alias: ")
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
        word = input('')
        mqttc.publish(userdata['mychannel'], f'W{word}')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
