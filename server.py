########################################################################################
########################################################################################
###############                                                          ###############
###############            PRÃCTICA 3 - PROGRAMACIÃN PARALELA            ###############
###############                   Cristina Ãvila Santos                  ###############
###############                   Isabel BeltrÃ¡ Merino                   ###############
###############                   Claudia ViÃ±as JÃ¡Ã±ez                    ###############
###############                                                          ###############
########################################################################################
########################################################################################

from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep
from multiprocessing import Lock
import random
import sys

long = 5
filename = "palabras.txt"
public_topic = 'clients/cvinas/wordle'

def read_words(filename, long):
    lista = []
    f = open(filename, 'r')
    linea = f.readline()
    while linea != '':
        if len(linea) - 1 == long:
            lista.append(linea.strip())
        linea = f.readline()
    f.close()
    return lista
    
def elegir_palabra(filename, long):
    lista = read_words(filename, long)
    a = random.randint(0, len(lista) - 1)
    palabra = lista[a]
    return palabra

solution = elegir_palabra(filename, long)
print(f'La palabra elegida es {solution}')

def transformar_en_codigo(palabra1, palabra2):
    codigo = ''
    palabra1_ = palabra1.lower()
    palabra2_ = palabra2.lower()
    palabra1_lista = list(palabra1_)
    palabra2_lista = list(palabra2_)
    
    for i in range(len(palabra1_lista)):
        if palabra2_lista[i] == palabra1_lista[i]:
            codigo += '0 '
        elif palabra2_lista[i] != palabra1_lista[i] and palabra2_lista[i] in palabra1_lista:
            codigo += '1 '
        elif not(palabra2_lista[i] in palabra1_lista):
            codigo += '2 '
            
    return codigo

def el_topic_es_privado(topicc):
    string = 'clients/cvinas/wordle/'
    for i in range(22):
        try:
            if topicc[i] == string[i]:
                pass
            else:
                return False
        except:
            return False
    return True

def on_message_client(mqttc, userdata, msg):
    mutex = Lock()
    mutex.acquire()
    
    mensaje = msg.payload.decode('utf-8')
    if el_topic_es_privado(msg.topic) and mensaje[0] == 'W':
        palabra = mensaje[1:]
        try:
            #print(msg.payload) por aqui pasa
            if len(palabra) != long:
                mssg = f'M{palabra} -> La palabra debe tener {long} letras'
                mqttc.publish(public_topic, mssg)
            elif palabra.lower() != solution.lower():
                codigo = transformar_en_codigo(solution, palabra)
                mssg = f'M{palabra} -> {codigo}'
                mqttc.publish(public_topic, mssg)
            else:
                winner = msg.topic
                mqttc.publish(public_topic, f'MLa palabra era {solution}, {winner[22:]} ha ganado la partida')
                #userdata['status'] == 0
        finally:
            mutex.release()
    else:
        pass
        #print(msg.topic, msg.payload) por aqui pasa
            
            
def client_manager(msg, userdata, broker):
    #userdata = {'status': 1} #si el status estÃ¡ a 1, la partida estÃ¡ iniciada, cuando se pone en 0 la partida se acaba.
    mqttc = Client(userdata = userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message_client
    #mqttc.on_log = on_log
    mqttc.connect(broker)
    
    channel = msg.decode('utf-8')
    mqttc.subscribe(f'clients/cvinas/wordle/{channel[1:]}')
    mqttc.loop_forever()
    """
    if userdata['status'] == 0:
        mqttc.disconnect(broker)
    """


def on_message(mqttc, userdata, msg):
    if msg.topic == userdata['public_ch']:
        worker = Process(target = client_manager, args = (msg.payload, userdata, broker))
        worker.start()
    else:
        pass

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def main(broker):    
    userdata = {
        'broker': broker,
        'public_ch' : 'clients/cvinas/wordle'
    }
    mqttc = Client(userdata = userdata)
    mqttc.enable_logger()
    mqttc.connect(broker)
    mqttc.subscribe(userdata['public_ch'])
    mqttc.on_message = on_message
    #mqttc.on_log = on_log

    mqttc.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)