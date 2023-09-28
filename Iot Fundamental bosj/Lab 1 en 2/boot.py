# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#imports
import network
from secret import wifissid, wifipassword


# Flag om bij te houden of de network config al is afgedrukt
network_config_printed = False

#
#
# functie read_BME_data
def read_bme_data():
    import bmeboot  # Importeer bmeboot waar de functie is gedefinieerd

#
#
# functie wifi connect
def do_connect():
    global network_config_printed  # Gebruik de global variabele

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifissid, wifipassword)
        while not wlan.isconnected():
            pass
        
        if not network_config_printed:
            print('network config:', wlan.ifconfig())
            network_config_printed = True  # Markeer als afgedrukt na de eerste keer



#
# functie aan roepen
#
do_connect()
# read_bme_data()  # Roep de functie aan om BME280-gegevens te lezen

# Import and run your MQTT and BME280 script here
import bmemqtt