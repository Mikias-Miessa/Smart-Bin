import random
import json
import mysql.connector
from paho.mqtt import client as mqtt_client


broker = 'uda77bc3.emqx.cloud'
port = 1883
topic = "distanceData"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'mqtt'
password = 'Mqtt123'

# MySQL database configuration
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = ''
mysql_database = 'smart_trash'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        if message != '1':
            print(f"Received {message} from {msg.topic} topic")
            print(type(message))
        # Parse the JSON message
            try:
                data = json.loads(message)
                bin_id = data['bin_id']
                level = data['level']
                location = data['location']
                if float(level) >= 100:
                    level = 100

                # Store the data in the MySQL database
                store_data_in_database(bin_id, level, location)

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON message: {e}")
            except KeyError as e:
                print(f"Missing required data field: {e}")

    client.subscribe(topic)
    client.on_message = on_message


def store_data_in_database(bin_id, level, location):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = conn.cursor()

        # Insert the data into the table or update if bin_id already exists
        query = """
        INSERT INTO bins (bin_id, level, location)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        level = VALUES(level),
        location = VALUES(location)
        """
        values = (bin_id, level, location)
        cursor.execute(query, values)

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data stored in the database successfully")

    except mysql.connector.Error as error:
        print(f"Failed to store data in the database: {error}")



def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()