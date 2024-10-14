import machine
import ssd1306
import math
import time

# Configuración del potenciómetro
pot = machine.ADC(machine.Pin(32))  # Asegúrate de que el pin sea el correcto (GPIO 32)

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

# Función para dibujar un arco con mayor grosor
def draw_thick_arc(cx, cy, radius, start_angle, end_angle, thickness=2):
    for t in range(thickness):
        for angle in range(start_angle, end_angle + 1):
            angle_rad = math.radians(angle)
            x = int(cx - (radius + t) * math.cos(angle_rad))
            y = int(cy - (radius - t) * math.sin(angle_rad))  # "-radius" para coordinar con el eje Y de la pantalla
            oled.pixel(x, y, 1)

# Función para dibujar marcas de referencia en el gauge
def draw_gauge_marks(cx, cy, radius):
    for angle in range(0, 181, 30):  # Marcas cada 30 grados
        angle_rad = math.radians(angle)
        x_start = int(cx + (radius - 5) * math.cos(angle_rad))
        y_start = int(cy - (radius - 5) * math.sin(angle_rad))
        x_end = int(cx + radius * math.cos(angle_rad))
        y_end = int(cy - radius * math.sin(angle_rad))
        oled.line(x_start, y_start, x_end, y_end, 1)

# Función para mostrar un número grande en el centro
def draw_large_text(cx, cy, text):
    for i, char in enumerate(text):
        x_offset = i * 14 - 7 * len(text)  # Ajuste para que los números estén más juntos
        oled.text(char, cx + x_offset, cy, 1)

def mostrar_gauge_circular():
    while True:
        # Leer el valor del potenciómetro (rango de 0 a 4095)
        valor = pot.read()

        # Convertir el valor a un ángulo (0 a 180 grados)
        angle = int((valor / 4095) * 180)

        # Convertir el valor a porcentaje
        porcentaje = int((valor / 4095) * 100)

        # Limpiar la pantalla
        oled.fill(0)

        # Coordenadas del centro del círculo y radio
        cx, cy = 64, 40
        radius = 30

        # Dibujar el contorno del gauge
        draw_gauge_marks(cx, cy, radius)

        # Dibujar el arco que representa el valor del potenciómetro con grosor
        draw_thick_arc(cx, cy, radius, 0, angle, thickness=3)

        # Mostrar el valor en el centro como número grande, más abajo
        draw_large_text(cx - 8, cy + 5, str(porcentaje))  # Ajustado más abajo y a la derecha
        oled.text('%', cx + 24, cy + 5, 1)  # Símbolo de porcentaje más junto

        # Actualizar la pantalla
        oled.show()

        # Esperar un momento antes de leer nuevamente
        time.sleep(0.1)

# Ejecutar la función para mostrar el gauge circular estilizado con número grande y símbolo de porcentaje
mostrar_gauge_circular()
