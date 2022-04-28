from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep
from multiprocessing import Lock
import random
import sys

#####################################################################################################
long = 5
filename = "palabras.txt"

def read_words(filename, long): #convierte el fichero de palabras en una lista de palabras de longitud 5
    lista = []
    f = open(filename, 'r')
    linea = f.readline()
    while linea != '':
        if len(linea) - 1 == long:
            lista.append(linea.strip())
        linea = f.readline()
    f.close()
    return lista
    
def elegir_palabra(filename, long): #elige una palabra aleatoria de la lista
    lista = read_words(filename, long)
    a = random.randint(0, len(lista) - 1)
    palabra = lista[a]
    return palabra

solution = elegir_palabra(filename, long)
print(f'La palabra elegida es {solution}')

def transformar_en_codigo(palabra1, palabra2): #palabra1 y palabra2 son cadenas de caracteres.
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

#####################################################################################################

public_topic = 'clients/cvinas/wordle'


def on_message_client(mqttc, userdata, msg):
    mutex = Lock()
    mutex.acquire()
    
    mensaje = msg.payload.decode('utf-8')
    palabra = mensaje[1:]
    try:
        #print(msg.payload) por aqui pasa
        if len(palabra) != long:
            mssg = f'{palabra} -> La palabra debe tener {long} letras'
            mqttc.publish(public_topic, mssg)
        elif palabra != solution:
            codigo = transformar_en_codigo(solution, palabra)
            mssg = f'{palabra} -> {codigo}'
            mqttc.publish(public_topic, mssg)
        else:
            mqttc.publish(public_topic, f'Partida finalizada. La palabra era {solution}')
            winner = msg.topic
            mqttc.publish(public_topic, f'{winner[22:]} ha ganado la partida')
            #userdata['status'] == 0
    finally:
        mutex.release()
    #print(msg.topic, msg.payload) por aqui pasa

    
    """
        if el_topic_es_privado(msg.topic):
        mensaje = msg.payload.decode('utf-8')
        print(mensaje)
        if tipo_de_mensaje(mensaje) == 1:
            nombre = mensaje[1:]
            print(f'{mensaje} se ha unido a la partida')
        elif tipo_de_mensaje(mensaje) == 2:
      """      
            
            
def client_manager(msg, userdata, broker):
    #userdata = {'status': 1} #si el status estÃ¡ a 1, la partida estÃ¡ iniciada, cuando se pone en 0 la partida se acaba.
    mqttc = Client(userdata = userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message_client
    #mqttc.on_log = on_log
    mqttc.connect(broker)
    
    
    
    channel = msg.decode('utf-8') #no entiendo por que no es msg.playload.decode('utf-8')
    mqttc.subscribe(f'clients/cvinas/wordle/{channel[1:]}')
    if channel[0] == 'N':
        print(f'{channel[1:]} se ha unido a la partida')
        
    mqttc.loop_forever()
    """
    if userdata['status'] == 0:
        mqttc.disconnect(broker)
"""
        
def el_topic_es_privado(topicc):
    canal = 'clients/cvinas/wordle/'
    for i in range(22):
        try:
            if topicc[i] == canal[i]:
                pass
            else:
                return False
        except:
            return False
    return True

def tipo_de_mensaje(string): #tipo = 1 es nombre, tipo=2 es palabra a probar
    tipo = 0
    if string[0] == 'N':
        tipo = 1
    elif string[0] == 'W':
        tipo = 2
    return tipo
    
#ON_MESSAGE ES LA FUNCIÃN DE REACCIÃN A UN MENSAJE.
def on_message(mqttc, userdata, msg):
    #print('on_message', msg.topic, msg.payload)
    if msg.topic == userdata['public_ch']:
        worker = Process(target = client_manager, args = (msg.payload, userdata, broker))
        worker.start()
    #print('end on_message', msg.payload)

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
    mqttc.subscribe('clients/cvinas/wordle')
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
