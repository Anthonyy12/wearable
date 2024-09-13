import machine
import ssd1306
import dht
import math
import time

# Configuración del sensor DHT22
sensor = dht.DHT22(machine.Pin(32))

# Configuración del OLED display
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Función para dibujar un círculo
def draw_circle(cx, cy, radius, color=1):
    for angle in range(0, 360):
        angle_rad = math.radians(angle)
        x = int(cx + radius * math.cos(angle_rad))
        y = int(cy + radius * math.sin(angle_rad))
        oled.pixel(x, y, color)

# Función para dibujar un arco grueso
def draw_thick_arc(cx, cy, radius, start_angle, end_angle, thickness=2):
    for t in range(thickness):
        for angle in range(start_angle, end_angle + 1):
            angle_rad = math.radians(angle)
            x = int(cx + (radius - t) * math.cos(angle_rad))
            y = int(cy - (radius - t) * math.sin(angle_rad))
            oled.pixel(x, y, 1)

# Función para dibujar marcas de referencia en el gauge
def draw_gauge_marks(cx, cy, radius):
    for angle in range(-90, 91, 30):  # Marcas cada 30 grados
        angle_rad = math.radians(angle)
        x_start = int(cx + (radius - 4) * math.cos(angle_rad))
        y_start = int(cy - (radius - 4) * math.sin(angle_rad))
        x_end = int(cx + (radius - 1) * math.cos(angle_rad))
        y_end = int(cy - (radius - 1) * math.sin(angle_rad))
        oled.line(x_start, y_start, x_end, y_end, 1)

# Función para dibujar el termómetro
def draw_thermometer(cx, cy, min_temp, max_temp, current_temp):
    oled.rect(cx - 8, cy - 30, 16, 60, 1)  # Termómetro más pequeño
    temp_range = max_temp - min_temp
    fill_height = int(((current_temp - min_temp) / temp_range) * 60)
    oled.fill_rect(cx - 7, cy + 30 - fill_height, 14, fill_height, 1)  # Relleno del termómetro
    oled.text(f'{current_temp:.1f}C', cx - 15, cy + 35, 1)  # Mostrar temperatura ajustada

# Función para mostrar la humedad en un gauge circular
def draw_humidity_gauge(cx, cy, radius, humidity):
    draw_circle(cx, cy, radius)  # Contorno del gauge
    draw_gauge_marks(cx, cy, radius)  # Marcas de referencia
    end_angle = int((humidity / 100) * 180) - 90  # Escala de 0 a 100% mapeada a 180 grados
    draw_thick_arc(cx, cy, radius, -90, end_angle, thickness=2)  # Arco que representa la humedad
    oled.text(f'Hum: {humidity:.0f}%', cx - 55, cy - 5, 1)  # Mostrar humedad ajustada en el centro

def mostrar_graficas():
    while True:
        # Leer valores del sensor DHT22
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()

        # Limpiar la pantalla
        oled.fill(0)

        # Coordenadas y configuración
        cx_temp, cy_temp = 30, 32  # Ajustar coordenadas del termómetro
        cx_humid, cy_humid = 96, 32
        min_temp, max_temp = -40, 80  # Rango de temperaturas que soporta el DHT22
        radius = 16  # Radio reducido para el gauge de humedad

        # Dibujar termómetro y gauge de humedad
        draw_thermometer(cx_temp, cy_temp, min_temp, max_temp, temperatura)
        draw_humidity_gauge(cx_humid, cy_humid, radius, humedad)

        # Mostrar el valor de la temperatura junto al termómetro
        oled.text(f'Temp: {temperatura:.1f}C', 40, 0, 1)

        # Actualizar la pantalla
        oled.show()

        # Esperar un momento antes de leer nuevamente
        time.sleep(2)

# Ejecutar la función para mostrar las gráficas
mostrar_graficas()
