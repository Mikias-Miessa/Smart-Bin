import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    # This function will be called when a message is received
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

broker_address = "06c84745277c47e5a6a5fa9c6981d8fd.s2.eu.hivemq.cloud"  # Replace with the actual broker address
broker_port = 8883  # Replace with the correct port number for your MQTT broker

# Set username and password
username = "mikias"
password = "1038788520aA+"
client.username_pw_set(username, password)

client.connect(broker_address, broker_port)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

topic = "test"  # Replace with the topic you want to subscribe to
client.loop_start()
client.subscribe(topic)

while True:
    pass

client.loop_stop()
client.disconnect()
