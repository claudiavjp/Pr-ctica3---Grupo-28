from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep


def on_message_client(mqttc, userdata, msg):
    print(msg.topic, msg.payload)

def client_manager(msg, broker):
    userdata = {'status': 0}
    mqttc = Client(userdata=userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message_client
    mqttc.on_log = on_log
    mqttc.connect(broker)

    channel = msg.decode('utf-8')
    mqttc.subscribe(f'clients/cvinas/wordle/{channel}')
    mqttc.loop_start()
    while userdata['status'] == 0:
        pass


def on_message(mqttc, userdata, msg):
    print('on_message', msg.topic, msg.payload)
    if msg.topic == userdata['public_ch']:
        worker = Process(target=client_manager, args=(msg.payload, userdata['broker']))
        worker.start()
    print('end on_message', msg.payload)

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def main(broker):
    userdata = {
        'broker': broker,
        'public_ch' : 'clients/cvinas/wordle'
    }
    mqttc = Client(userdata=userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)

    mqttc.subscribe(userdata['public_ch'])

    mqttc.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
