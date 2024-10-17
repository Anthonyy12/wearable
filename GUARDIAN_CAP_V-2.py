import machine
import utime
import uasyncio as asyncio
from umqtt.robust import MQTTClient
import network
import urequests as requests
import ssd1306
import gc

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.addr = addr
        self.i2c = i2c
        self.i2c.writeto(self.addr, bytearray([107, 0]))  # Activar el MPU6050

    def read_accel_data(self):
        raw_data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        return self._convert_accel_data(raw_data)

    def read_gyro_data(self):
        raw_data = self.i2c.readfrom_mem(self.addr, 0x43, 6)
        return self._convert_gyro_data(raw_data)

    def _convert_accel_data(self, raw_data):
        x = self._convert_to_int16(raw_data[0:2])
        y = self._convert_to_int16(raw_data[2:4])
        z = self._convert_to_int16(raw_data[4:6])
        return {"x": x, "y": y, "z": z}

    def _convert_gyro_data(self, raw_data):
        x = self._convert_to_int16(raw_data[0:2])
        y = self._convert_to_int16(raw_data[2:4])
        z = self._convert_to_int16(raw_data[4:6])
        return {"x": x, "y": y, "z": z}

    def _convert_to_int16(self, data):
        value = (data[0] << 8) | data[1]
        if value > 32767:
            value -= 65536
        return value

# Configuración de la red Wi-Fi
SSID = 'Megacable_6WHfTP3'
PASSWORD = 'VmAVguPemQ37fX7CS9'

# Configuración de Firebase
FIREBASE_URL = 'https://signos-zodical-default-rtdb.firebaseio.com/datos.json'

# Configuración MQTT
MQTT_BROKER = 'broker.hivemq.com'
MQTT_CLIENT_ID = 'Saldana'

# Pines de los sensores
TRIG_PIN = 5      # Pin para TRIG del sensor HC-SR04
ECHO_PIN = 18     # Pin para ECHO del sensor HC-SR04
LDR_PIN = 34      # Pin para la fotorresistencia
BUZZER_PIN = 23   # Pin para el buzzer
BUZZER_PIN_19 = 19  # Pin para el segundo buzzer
LED_R_PIN = 25  # Pin para el LED rojo
LED_G_PIN = 26  # Pin para el LED verde
LED_B_PIN = 27  # Pin para el LED azul
MQ2_PIN = 35  # Definir el pin ADC para el sensor MQ-2


# Pines para la pantalla OLED (I2C)
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

LED_PIN = 4

# Umbral de distancia
DISTANCIA_UMBRAL = 50  # en centímetros

# Inicializar pantalla OLED, sensores y actuadores
i2c = machine.SoftI2C(scl=machine.Pin(I2C_SCL_PIN), sda=machine.Pin(I2C_SDA_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # Pantalla de 128x64 píxeles
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)
buzzer_19 = machine.Pin(BUZZER_PIN_19, machine.Pin.OUT)
ldr = machine.ADC(machine.Pin(LDR_PIN))
ldr.atten(machine.ADC.ATTN_11DB)  # Escala de 3.3V
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led_r = machine.Pin(LED_R_PIN, machine.Pin.OUT)
led_g = machine.Pin(LED_G_PIN, machine.Pin.OUT)
led_b = machine.Pin(LED_B_PIN, machine.Pin.OUT)
mq2 = machine.ADC(machine.Pin(MQ2_PIN))
mq2.atten(machine.ADC.ATTN_11DB)  # Configurar la escala a 3.3V


# Inicializar el sensor MPU6050
mpu = MPU6050(i2c)

# Listas para almacenar los últimos valores de los sensores (hasta 128 puntos)
historico_distancia = []
historico_luz = []
historico_accel = []  # Para almacenar datos del acelerómetro



async def leer_mq2():
    try:
        return mq2.read()
    except Exception as e:
        print('Error en leer MQ-2:', e)
        return None


# Función para calcular el promedio de los valores del acelerómetro
def calcular_promedio_accel(historico):
    if not historico:
        return None
    avg_x = sum(d['x'] for d in historico) / len(historico)
    avg_y = sum(d['y'] for d in historico) / len(historico)
    avg_z = sum(d['z'] for d in historico) / len(historico)
    return avg_x, avg_y, avg_z

def controlar_led_rgb(promedio):
    if promedio:
        avg_x, avg_y, avg_z = promedio
        
        # Ejemplo de lógica para cambiar el color del LED según el promedio
        if avg_x > 0:
            led_r.value(1)  # Enciende el LED rojo
            led_g.value(0)
            led_b.value(0)
        elif avg_y > 0:
            led_r.value(0)
            led_g.value(1)  # Enciende el LED verde
            led_b.value(0)
        elif avg_z > 0:
            led_r.value(0)
            led_g.value(0)
            led_b.value(1)  # Enciende el LED azul
        else:
            led_r.value(0)  # Apagar LED si no hay movimiento
            led_g.value(0)
            led_b.value(0)
            
estado_buzzer1 = False
estado_buzzer2 = False
estado_oled = False
estado_led_rgb = True
estado_led = True

# Mostrar valores en la pantalla OLED (asincrónicamente)
async def mostrar_datos_oled(distancia, luz, acelerometro):
    global estado_oled
    if estado_oled:  # Solo actualiza si OLED está encendida
        oled.fill(0)  # Limpiar pantalla completa
        oled.text(f"Dist: {distancia:.2f} cm", 0, 0)
        oled.text(f"Luz: {luz}", 0, 10)

        if acelerometro:
            oled.text(f"Acc X: {acelerometro['x']}", 0, 20)
            oled.text(f"Acc Y: {acelerometro['y']}", 0, 30)
            oled.text(f"Acc Z: {acelerometro['z']}", 0, 40)
        else:
            oled.text("Acc: Error", 0, 20)

        oled.show()
    else:
        oled.fill(0)  # Mantener la pantalla apagada
        oled.show()

# Configurar la conexión Wi-Fi de manera asincrónica
async def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        print('Conectando a Wi-Fi...')
        await asyncio.sleep(1)  # Esperar de manera asincrónica

    print('Conectado a Wi-Fi:', wlan.ifconfig())

# Medir distancia del sensor ultrasónico (asincrónicamente)
async def medir_distancia():
    trig.value(0)
    await asyncio.sleep(0.000002)
    trig.value(1)
    await asyncio.sleep(0.00001)
    trig.value(0)
    pulso_inicio, pulso_fin = 0, 0
    while echo.value() == 0:
        pulso_inicio = utime.ticks_us()
    while echo.value() == 1:
        pulso_fin = utime.ticks_us()
    duracion = utime.ticks_diff(pulso_fin, pulso_inicio)
    return (duracion * 0.0343) / 2

# Leer valor de fotorresistencia (asincrónicamente)
async def leer_fotorresistencia():
    try:
        return ldr.read()
    except Exception as e:
        print('Error en leer fotorresistencia:', e)
        return None  # O maneja el error de otra manera

# Leer datos del acelerómetro (asincrónicamente)
async def leer_acelerometro():
    accel = mpu.read_accel_data()
    historico_accel.append(accel)
    if len(historico_accel) > 10:
        historico_accel.pop(0)
    return accel

# Controlar el buzzer de forma asincrónica
async def controlar_buzzer(distancia):
    global buzzer_count
    if distancia < DISTANCIA_UMBRAL:
        buzzer.value(1)
    else:
        buzzer.value(0)

        

# Función para tocar una melodía en el buzzer
# Función para tocar una melodía en el buzzer
async def tocar_melodia():
    melodía = [
        (440, 200),  # La (A) 440Hz por 200ms
        (494, 200),  # Si (B) 494Hz por 200ms
        (523, 200),  # Do (C) 523Hz por 200ms
        (587, 200),  # Re (D) 587Hz por 200ms
    ]

    for frecuencia, duracion in melodía:
        buzzer_19.value(1)  # Encender buzzer en pin 19
        utime.sleep(duracion / 1000)  # Esperar la duración en segundos
        buzzer_19.value(0)  # Apagar buzzer
        await asyncio.sleep(0.05)  # Pausa de 50ms entre notas


# Publicar en MQTT para cada sensor
async def publicar_mqtt(client, distancia, luz, acelerometro, mq2_value):
    try:
        client.publish('sensores/distancia', str(distancia))
        client.publish('sensores/luz', str(luz))
        if acelerometro:
            mensaje_acelerometro = "{},{},{}".format(acelerometro['x'], acelerometro['y'], acelerometro['z'])
            client.publish('sensores/acelerometro', mensaje_acelerometro)
        if mq2_value is not None:
            client.publish('sensores/mq2', str(mq2_value))  # Publicar el valor del sensor MQ-2
    except Exception as e:
        print('Error en MQTT:', e)
        
# Variables para mantener el estado de los actuadores


async def controlar_actuadores_mqtt(client):
    global estado_buzzer1, estado_buzzer2, estado_oled, estado_led_rgb, estado_led

    def on_message(topic, msg):
        global estado_buzzer1, estado_buzzer2, estado_oled, estado_led_rgb, estado_led

        if topic == b'actuador/buzzer1':
            buzzer.value(1 if msg == b'on' else 0)
            estado_buzzer1 = (msg == b'on')
        elif topic == b'actuador/buzzer2':
            buzzer_19.value(1 if msg == b'on' else 0)
            estado_buzzer2 = (msg == b'on')
        elif topic == b'actuador/led_rgb':
            led_r.value(1 if msg == b'on' else 0)
            led_g.value(0)
            led_b.value(0)
            estado_led_rgb = (msg == b'on')
        elif topic == b'actuador/led':
            led.value(1 if msg == b'on' else 0)
            estado_led = (msg == b'on')
        elif topic == b'actuador/oled':  # Controlar OLED desde MQTT
            estado_oled = (msg == b'on')  # Actualizar el estado de la OLED
            if not estado_oled:
                oled.fill(0)
                oled.show()

    client.set_callback(on_message)
    client.subscribe('actuador/buzzer1')
    client.subscribe('actuador/buzzer2')
    client.subscribe('actuador/led_rgb')
    client.subscribe('actuador/led')
    client.subscribe('actuador/oled')  # Suscribir al tópico de control de la OLED

    while True:
        client.check_msg()
        await asyncio.sleep(0.1)


# Publicar en Firebase
async def publicar_firebase(distancia, luz, acelerometro):
    datos = {
        'distancia': distancia,
        'luz': luz,
        # Solo enviar valores simples en lugar del objeto completo
        'accel_x': acelerometro['x'],
        'accel_y': acelerometro['y'],
        'accel_z': acelerometro['z']
    }
    try:
        gc.collect()
        response = requests.post(FIREBASE_URL, json=datos)
        print('Datos enviados a Firebase:', response.text)
    except Exception as e:
        print('Error al publicar en Firebase:', e)

        
def verificar_luz(luz_actual):
    # Almacenar el valor actual en el histórico
    historico_luz.append(luz_actual)

    # Mantener solo los últimos dos registros
    if len(historico_luz) > 2:
        historico_luz.pop(0)

    # Calcular la suma de los últimos dos registros
    if len(historico_luz) == 2:
        suma_luz = sum(historico_luz)
        print(f"Suma de los últimos dos registros de luz: {suma_luz}")
        
        # Encender el LED si la suma es mayor a 500
        if suma_luz > 3500:
            led.value(1)  # Encender el LED
            print("LED encendido")
        else:
            led.value(0)  # Apagar el LED
            print("LED apagado")

# Función principal que coordina las lecturas y publicaciones
async def main():
    await conectar_wifi()
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()

    # Iniciar el control de actuadores mediante MQTT
    asyncio.create_task(controlar_actuadores_mqtt(client))

    while True:
        distancia = await medir_distancia()
        luz = ldr.read()
        acelerometro = await leer_acelerometro()

        if distancia is not None and luz is not None and acelerometro is not None:
            await mostrar_datos_oled(distancia, luz, acelerometro)  # Solo si la OLED está encendida
            await publicar_mqtt(client, distancia, luz, acelerometro, await leer_mq2())
            await publicar_firebase(distancia, luz, acelerometro)
            await controlar_buzzer(distancia)
            promedio_accel = calcular_promedio_accel(historico_accel)
            controlar_led_rgb(promedio_accel)
            verificar_luz(luz)

        await asyncio.sleep(0.3)

# Ejecutar el programa
asyncio.run(main())