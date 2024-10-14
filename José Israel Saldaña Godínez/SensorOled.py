import machine
import dht
import time
import network
import ubinascii
from umqtt.simple import MQTTClient

# Clase para manejar el sensor ultrasónico HC-SR04
class HCSR04:
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=10000):
        self.trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)
        self.echo_timeout_us = echo_timeout_us

    def _send_pulse_and_wait(self):
        self.trigger.off()
        time.sleep_us(5)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            return -1

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        if pulse_time < 0:
            return -1
        distance = (pulse_time / 2) / 29.1  # Velocidad del sonido en el aire es aprox. 343 m/s
        return distance

# Configuración de la red WiFi
SSID = 'Megacable_6WHfTP3'  # Cambia esto por tu nombre de red
PASSWORD = 'VmAVguPemQ37fX7CS9'  # Cambia esto por tu contraseña
MQTT_BROKER = 'broker.hivemq.com'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# Pines de conexión
dht_pin = machine.Pin(15)
dht_sensor = dht.DHT11(dht_pin)

# Sensor ultrasonico
ultrasonic = HCSR04(trigger_pin=5, echo_pin=18)

# Conectar a WiFi
def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(SSID, PASSWORD)
    while not station.isconnected():
        pass
    print('Conexión WiFi establecida')

# Publicar datos en MQTT
def mqtt_publish(topic, msg):
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.connect()
    client.publish(topic, msg)
    client.disconnect()

# Conexión WiFi
connect_wifi()

while True:
    try:
        # Leer sensor DHT11
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        # Leer distancia del sensor ultrasónico
        distance = ultrasonic.distance_cm()

        # Mostrar datos en el monitor serie
        print("Temperatura: {}C".format(temp))
        print("Humedad: {}%".format(hum))
        print("Distancia: {:.2f}cm".format(distance))

        # Publicar en MQTT
        mqtt_publish("sensor/temperature", str(temp))
        mqtt_publish("sensor/humidity", str(hum))
        mqtt_publish("sensor/distance", str(distance))

        time.sleep(1)  # Esperar 5 segundos entre lecturas

    except OSError as e:
        print("Error al leer los sensores:", e)
