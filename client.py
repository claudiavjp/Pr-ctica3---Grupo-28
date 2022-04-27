from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep


def on_message(mqttc, userdata, msg):
    print('on_message', msg.topic, msg.payload)
    if msg.topic == userdata['mychannel']:
        print(msg.payload)
    #worker = Process(target = work_on_message, args = (str(msg.payload), userdata['broker']))
    #worker.start()
    print('end on_message', msg.payload)

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def get_name():
    name = input("dame el tu alias: ")
    return name

def main(broker):
    userdata = {
        'broker': broker,
        'mychannel' : ''
    }
    mqttc = Client(userdata=userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)

    topic = 'clients/cvinas/wordle'
    mqttc.subscribe(topic)
    myname = get_name()
    mqttc.publish(topic, f"{myname}")
    userdata['mychannel'] = f'{topic}/{myname}'
    mqttc.subscribe(userdata['mychannel'])

    mqttc.loop_start()
    while True:
        word = input('dame una palabra: ')
        mqttc.publish(userdata['mychannel'], word)

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
