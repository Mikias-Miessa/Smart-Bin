import paho.mqtt.client as mqtt

# Callback function when connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {rc}")
    # Subscribe to the desired topic after connection is established
    client.subscribe("test")  # Replace "your_topic" with the topic you want to subscribe to

# Callback function when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# Set username and password
client.username_pw_set("mikias", "1038788520aA+")

# Connect to the MQTT broker
client.connect("06c84745277c47e5a6a5fa9c6981d8fd.s2.eu.hivemq.cloud", 8883)

# Start the MQTT network loop to handle incoming and outgoing messages
client.loop_forever()
