import machine
import utime
import uasyncio as asyncio
from umqtt.robust import MQTTClient
import network
import urequests as requests
import ssd1306

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

# Pines para la pantalla OLED (I2C)
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

LED_PIN = 4

# Umbral de distancia
DISTANCIA_UMBRAL = 80  # en centímetros

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

# Inicializar el sensor MPU6050
mpu = MPU6050(i2c)

# Listas para almacenar los últimos valores de los sensores (hasta 128 puntos)
historico_distancia = []
historico_luz = []
historico_accel = []  # Para almacenar datos del acelerómetro


# Variables para el contador del buzzer
buzzer_count = 0  # Contador de las veces que suena el buzzer


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

# Mostrar valores en la pantalla OLED (asincrónicamente)
async def mostrar_datos_oled(distancia, luz, acelerometro):
    oled.fill(0)  # Limpiar pantalla completa
    oled.text(f"Dist: {distancia:.2f} cm", 0, 0)
    oled.text(f"Luz: {luz}", 0, 10)
    
    # Asegurarse de que acelerometro no sea None
    if acelerometro:
        oled.text(f"Acc X: {acelerometro['x']}", 0, 20)
        oled.text(f"Acc Y: {acelerometro['y']}", 0, 30)
        oled.text(f"Acc Z: {acelerometro['z']}", 0, 40)
    else:
        oled.text("Acc: Error", 0, 20)

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
    try:
        trig.value(0)
        await asyncio.sleep(0.000002)  # 2 microsegundos
        trig.value(1)
        await asyncio.sleep(0.00001)   # 10 microsegundos
        trig.value(0)

        # Esperar el pulso de ECHO
        while echo.value() == 0:
            pulso_inicio = utime.ticks_us()

        while echo.value() == 1:
            pulso_fin = utime.ticks_us()

        duracion = utime.ticks_diff(pulso_fin, pulso_inicio)
        distancia = (duracion * 0.0343) / 2
        return distancia
    except Exception as e:
        print('Error en medir distancia:', e)
        return None  # O maneja el error de otra manera

# Leer valor de fotorresistencia (asincrónicamente)
async def leer_fotorresistencia():
    try:
        return ldr.read()
    except Exception as e:
        print('Error en leer fotorresistencia:', e)
        return None  # O maneja el error de otra manera

# Leer datos del acelerómetro (asincrónicamente)
async def leer_acelerometro():
    try:
        accel = mpu.read_accel_data()  # Obtiene datos del acelerómetro
        historico_accel.append(accel)  # Agregar el valor al histórico

        # Mantener solo los últimos 10 registros
        if len(historico_accel) > 10:
            historico_accel.pop(0)

        return accel
    except Exception as e:
        print('Error en leer acelerómetro:', e)
        return None  # O maneja el error de otra manera

# Controlar el buzzer de forma asincrónica
# Controlar el buzzer de forma asincrónica
async def controlar_buzzer(distancia):
    global buzzer_count
    if distancia < DISTANCIA_UMBRAL:
        buzzer.value(1)  # Activar buzzer en pin 23
        buzzer_count += 1  # Incrementar el contador
        print("Distancia menor a 80 cm. Activando buzzer.")

        # Comprobar si el buzzer ha sonado 5 veces
        if buzzer_count == 5:
            print("El buzzer ha sonado 5 veces. Activando melodía.")
            buzzer.value(0)  # Apagar el buzzer en pin 23
            await tocar_melodia()  # Tocar melodía en buzzer del pin 19
            buzzer_count = 0  # Reiniciar contador
        else:
            await asyncio.sleep(0.5)  # Mantener el buzzer encendido por un tiempo corto
    else:
        buzzer.value(0)  # Desactivar buzzer si la distancia es mayor al umbral

        

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
async def publicar_mqtt(client, distancia, luz, acelerometro):
    try:
        # Publicar distancia en un tópico específico
        mensaje_distancia = str(distancia)  # Convertir el valor numérico a cadena antes de enviar
        client.publish('sensores/distancia', mensaje_distancia)
        print('Dato de distancia enviado a MQTT:', mensaje_distancia)

        # Publicar luz en un tópico específico
        mensaje_luz = str(luz)
        client.publish('sensores/luz', mensaje_luz)
        print('Datos de luz enviados a MQTT:', mensaje_luz)

        # Publicar acelerómetro en un tópico específico
        if acelerometro:
            # Formato "x,y,z"
            mensaje_acelerometro = "{},{},{}".format(acelerometro['x'], acelerometro['y'], acelerometro['z'])
            client.publish('sensores/acelerometro', mensaje_acelerometro)
            print('Datos del acelerómetro enviados a MQTT:', mensaje_acelerometro)
    except Exception as e:
        print('Error al publicar en MQTT:', e)


# Publicar en Firebase
async def publicar_firebase(distancia, luz, acelerometro):
    datos = {
        'distancia': distancia,
        'luz': luz,
        'acelerometro': acelerometro
    }
    try:
        # Cambiar la URL para usar el endpoint de 'push' que agrega un nuevo registro
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
    await conectar_wifi()  # Conectar a la red Wi-Fi

    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()

    while True:
        distancia = await medir_distancia()
        luz = await leer_fotorresistencia()
        acelerometro = await leer_acelerometro()

        if distancia is not None and luz is not None and acelerometro is not None:
            await mostrar_datos_oled(distancia, luz, acelerometro)
            await publicar_mqtt(client, distancia, luz, acelerometro)
            await publicar_firebase(distancia, luz, acelerometro)
            await controlar_buzzer(distancia)
            
            promedio_accel = calcular_promedio_accel(historico_accel)
            controlar_led_rgb(promedio_accel)  # Controlar el LED RGB

            # Verificar la luz actual
            verificar_luz(luz)

        await asyncio.sleep(0.1)  # Esperar un segundo antes de la próxima lectura

# Ejecutar la función principal
asyncio.run(main())
