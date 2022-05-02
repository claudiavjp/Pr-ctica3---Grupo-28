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
    print('Vamos a jugar al wordle. El objetivo es adivinar la palabra de 5 letras que estoy pensando. Para ello, tendrÃ¡s que ir lanzÃ¡ndome palabras de 5 letras. Yo te devolverÃ© una serie de 5 numeros segÃºn las letras de la palabra que has elegido estÃ¡n en mi palabra o no. Si pongo un 2, la letra no estÃ¡ en mi palabra; si pongo un 1 la letra estÃ¡ en la palbra pero en otra posiciÃ³n; y si pongo un 0 la letra estÃ¡ en la palabra y ademÃ¡s ocupa la misma posiciÃ³n que en tu palabra.\n')
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
