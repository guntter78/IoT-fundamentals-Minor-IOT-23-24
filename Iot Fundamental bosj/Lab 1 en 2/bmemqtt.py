# Imports
import network
import utime
from machine import Pin, I2C
from time import sleep
import BME280
from umqtt.simple import MQTTClient  # Importeer de MQTTClient
from mqttconf import mqtt_broker, mqtt_client_id, mqtt_password, mqtt_user, mqtt_topic 


# MQTT-configuratie
mqtt_topic = "sensor_data"  # Het MQTT-onderwerp om gegevens te publiceren

# WiFi-configuratie (uit secret.py)
from secret import wifissid, wifipassword

# Flag om bij te houden of de network config al is afgedrukt
network_config_printed = False

# Functie voor het lezen van BME280-gegevens
def read_bme_data():
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    return temp, hum, pres

# Functie om verbinding te maken met WiFi
def do_connect():
    global network_config_printed  # Gebruik de global variabele

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(wifissid, wifipassword)
        while not wlan.isconnected():
            pass

        if not network_config_printed:
            print('Network config:', wlan.ifconfig())
            network_config_printed = True  # Markeer als afgedrukt na de eerste keer

# Functie voor het publiceren van gegevens naar MQTT
def publish_mqtt_data(temp, hum, pres):
    try:
        client = MQTTClient(mqtt_client_id, mqtt_broker, user=mqtt_user, password=mqtt_password)
        client.connect()
        payload = "Temperature: {}°C, Humidity: {}%, Pressure: {}hPa".format(temp, hum, pres)
        client.publish(mqtt_topic, payload)
        client.disconnect()
    except Exception as e:
        print('Error publishing to MQTT:', str(e))

# Hoofdprogramma
do_connect()  # Maak verbinding met WiFi

# Teller voor het bijhouden van het aantal metingen
measurement_count = 0

# Aantal metingen dat je wilt uitvoeren (in dit geval 5)
total_measurements = 5

# Loop voor het uitvoeren van metingen
for _ in range(total_measurements):
    temp, hum, pres = read_bme_data()  # Lees BME280-gegevens
    print('#############')
    print(f'Measurement {measurement_count + 1}/{total_measurements}')
    print('Temperature:', temp)
    print('Humidity:', hum)
    print('Pressure:', pres)
    print('#############')
    
    # Publiceer gegevens naar MQTT
    publish_mqtt_data(temp, hum, pres)
    
    measurement_count += 1  # Update de teller
    
    if measurement_count < total_measurements:
        sleep(5)