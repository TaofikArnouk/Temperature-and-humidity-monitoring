import dht
import network
import urequests as requests
import machine
from time import sleep
import time

TOKEN = "BBFF-Y812UJG6ZyA3qLxG1FzcY5UpFi8oxa" #Put here your TOKEN
DEVICE_LABEL = "picowifiboard" # Assign the device label desire to be send
TEMPERATURE_LABEL = "temperature_sensor"  # Assign the variable label desire to be send
HUMIDITY_LABEL = "humidity_sensor"
WIFI_SSID = "Diana111" # Assign your the SSID of your network
WIFI_PASS = "Ayahatem?" # Assign your the password of your network

# Function for WiFi connection
def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(WIFI_SSID, WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip


# Builds the json to send the request
def build_json(variable, value):
    try:
        data = {variable: {"value": value}}
        return data
    except:
        return None

# Sending data to Ubidots Restful Webserice
def sendData(device, variable, value):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(variable, value)

        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

# Connect to the WiFi
connect()
tempSensor = dht.DHT11(machine.Pin(27))     # DHT11 Constructor 

# The code within the while loop would executed repeatedly due to the condition being set as ture
while True:
    tempSensor.measure()
    temperature = tempSensor.temperature()
    humidity = tempSensor.humidity()
    value = humidity
    returnValue = sendData(DEVICE_LABEL, HUMIDITY_LABEL, value)   
    value = temperature
    returnValue = sendData(DEVICE_LABEL, TEMPERATURE_LABEL, value)
    # Sends sensor data every 30 seconds 
    sleep(30)
