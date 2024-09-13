# Nombre del proyecto
## Guardian Cap

### Wearable
Realiza en equipo la lista de tareas necesarias para integrar un nuevo incremento o valor a tu proyecto wearable, favor de responder el Product Owner con su tablero en trello u otra herramienta las tareas priorizadas en el Sprint 01.

### Integrantes del equipo
* Cervantes Sanchez Sergio Abisay
* Domínguez Rosales Juan Antonio
* Saldaña Godíez José Israel

### Enunciado de visión
La gorra con sus sensores y funcionalidades proporcionaría a los invidentes herramientas adicionales para mejorar su seguridad, autonomía y calidad de vida. Con las alarmas, la localización y otras características, la gorra les ayudaría a evitar obstáculos, mantenerse informados sobre su entorno y tomar decisiones más informadas en su vida diaria. Además, la aplicación asociada permitiría una mayor interacción y personalización de la experiencia, brindando a los usuarios un mayor control sobre el uso y las preferencias de la gorra. El objetivo es utilizar la tecnología de la gorra y la aplicación asociada para brindar a las personas invidentes herramientas que les ayuden a moverse de manera más segura y confiable en su entorno, brindándoles mayor independencia y calidad de vida.

### Software empleado
| ID | Software | Version | Tipo |
|----|----------|---------|------|
| 1  | PlatformIO | 6.1.15 | Open Source |
| 2  | Visual Studio Code | 1.92.2  | Open Source |
| 3  | Firebase | -  | Freemium |
| 4  | EMQX Platform | 5.0  | Open Source |
| 5  | Flutter | 3.22.2  | Open Source |


### Hardware empleado
| ID  | Nombre                      | Descripción                                                                                                                              | Imagen | Costo Unitario | Cantidad |
|-----|-----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------:|--------|:--------------:|:--------:|
| 1   | ESP32                       | La ESP32 actuaría como el cerebro de la gorra inteligente, gestionando la conectividad, procesando los datos de los sensores y controlando la interacción con otros dispositivos para brindar una experiencia adaptada a las necesidades de las personas sordas. |  ![esp](https://github.com/Anthonyy12/wearable/blob/main/images/esp.jpg)      | $300           | 1        |
| 2   | DHT11                       | Podría medir la temperatura ambiente. Esto podría ser útil para proporcionar información sobre el clima y la temperatura a la persona sorda, ayudándola a adaptarse y tomar las precauciones necesarias. |   ![dht](https://github.com/Anthonyy12/wearable/blob/main/images/dht.png)     | $50            | 1        |
| 3   | HC-SR04                     | Puede detectar la presencia de objetos cercanos. Esto podría ser útil para alertar a la persona sorda sobre la presencia de obstáculos o personas cercanas, evitando posibles colisiones. |    ![hc](https://github.com/Anthonyy12/wearable/blob/main/images/hc.jpg)    | $50            | 1        |
| 4   | MPU6050                     | Sensor acelerómetro y giroscopio que puede detectar el movimiento y la orientación. Esto podría ayudar a la gorra inteligente a detectar el movimiento del usuario y proporcionar retroalimentación relevante. |   ![mpu](https://github.com/Anthonyy12/wearable/blob/main/images/mpu6050.jpg)     | $74           | 1        |
| 5   | Pantalla OLED 0.96"         | Pantalla de visualización para mostrar información al usuario, como el estado del dispositivo o alertas importantes. |   ![oled](https://github.com/Anthonyy12/wearable/blob/main/images/oled.jpg)     | $283           | 1        |
| 6   | Buzzer pasivo ARD-356        | Puede emitir sonidos como alertas auditivas para el usuario. Podría ser útil para notificaciones. |  ![buzzerpas](https://github.com/Anthonyy12/wearable/blob/main/images/buzzerpasivo.jpg)      | $29            | 1        |
| 7   | Buzzer                      | Similar al buzzer pasivo, puede emitir sonidos para notificaciones o alertas. |   ![buzzer](https://github.com/Anthonyy12/wearable/blob/main/images/buzzer.jpg)     | $15            | 1        |
| 8   | Mini Motor vibrador de 2v a 5v | Este motor vibrador puede proporcionar retroalimentación táctil para alertar a la persona sorda a través de vibraciones. |   ![mini](https://github.com/Anthonyy12/wearable/blob/main/images/mini.jpg)     | $32            | 1        |
| 9   | Transistor 2N2222           | Componente electrónico que podría usarse para controlar la corriente en diversos circuitos, como los que controlan los motores o los LEDs. |   ![trans](https://github.com/Anthonyy12/wearable/blob/main/images/trans.jpg)     | $5             | 1        |
| 10  | Diodo 1N4007                | Componente utilizado para evitar la inversión de corriente en los circuitos, protegiendo los componentes sensibles. |   ![diodo](https://github.com/Anthonyy12/wearable/blob/main/images/diodo.jpg)     | $2             | 1        |
| 11  | LED RGB                     | LED que emite luz de diferentes colores (Rojo, Verde, Azul), útil para indicar diferentes estados o alertas visuales. |   ![rgb](https://github.com/Anthonyy12/wearable/blob/main/images/rgb.jpg)     | $10            | 1        |
| 12  | Resistencias de 330 ohmios y 2k ohmios | Componentes necesarios para regular la corriente y proteger los componentes electrónicos. |   ![resistencias](https://github.com/Anthonyy12/wearable/blob/main/images/330.jpg)     | $1             | 2        |
| 13  | Cables jumper dupont         | Cables para realizar conexiones entre los diferentes componentes en el protoboard o circuito. |  ![jumpers](https://github.com/Anthonyy12/wearable/blob/main/images/jumpers.jpg)      | $117            | 10       |
| 14  | Baterías 12v                | Fuente de energía para alimentar los componentes de la gorra inteligente. |        | $50            | 1        |
| 15  | Regulador                   | Componente que regula el voltaje para mantener una alimentación estable para los componentes. |        | $15            | 1        |
| 16  | Rail de protoboard           | Utilizado para conectar los componentes electrónicos durante el desarrollo y pruebas del circuito. |   ![proto](https://github.com/Anthonyy12/wearable/blob/main/images/protoboard.jpg)     | $10            | 1        |



### Historias de usuario
|   ID   | Historia de Usuario | Prioridad | Estimación | Como probarlo | Responsable |
|--------|:-------------------:|-----------|:----------:|:-------------:|:-----------:|
| GCP001 | Como invidente, quiero poder detectar obstáculos en mi camino mientras uso la gorra para evitar accidentes. | Debe | 1 Día | Se puede probar colocando obstáculos en el camino del usuario y verificar si la gorra emite una señal de advertencia o vibra para alertar al usuario sobre la presencia del obstáculo. | Sergio |
| GCP002 | Como invidente, quiero poder ajustar el tamaño de la gorra para que se ajuste correctamente a mi cabeza. | Debe | 1 Día | Se puede probar proporcionando diferentes tamaños de gorra y verificar si el usuario puede ajustarla correctamente para obtener un ajuste cómodo y seguro. | Segio |
| GCP003 | Como invidente, quiero poder recibir información sobre la ubicación de objetos cercanos a mí mientras uso la gorra. | Debe | 2 Días | Se puede probar colocando objetos a diferentes distancias del usuario y verificar si la gorra emite señales o vibraciones proporcionales a la proximidad de los objetos. | Israel |
| GCP004 | Como invidente, quiero recibir información sobre la temperatura y la humedad actual cada cierto tiempo mientras uso la gorra. | Debe | 3 Días | Se puede probar conectando la gorra a una fuente de datos meteorológicos y verificar si la gorra proporciona información hablada o mediante vibraciones sobre el clima actual. | Israel |
| GCP005 | Como invidente, quiero recibir alertas de humedad para saber si debo tomar precauciones adicionales en caso de lluvia o condiciones húmedas mientras uso la gorra. | Debe | 3 Días | Se puede probar exponiendo la gorra a diferentes niveles de humedad y verificar si emite una alerta sonora cuando la humedad alcanza cierto umbral. | Antonio |
| GCP006 | Como invidente, quiero poder ajustar la sensibilidad del sensor de distancia en la gorra para adaptarlo a mis necesidades y entorno. | Debe | 2 Días | Se puede probar ajustando la sensibilidad del sensor de distancia en la gorra y verificar si las alarmas se activan adecuadamente cuando el usuario se acerca a objetos o paredes. | Antonio |
| GCP007 | Como invidente, quiero poder ajustar el volumen de las alarmas en la gorra para adaptarlo a mis preferencias auditivas. | Debe | 1 Día | 	Se puede probar ajustando el volumen de las alarmas en la gorra y verificar si el usuario puede escucharlas claramente sin que sean demasiado fuertes o suaves. | Antonio |
| GCP008 | Como invidente, quiero poder silenciar temporalmente las alarmas en la gorra cuando sea necesario. | Debe | 2 Días | Se puede probar activando una alarma en la gorra y luego verificar si el usuario puede silenciarla temporalmente sin desactivarla por completo. | Sergio |
| GCP009 | Como invidente, quiero saber mi pulso cardiaco en un dashboard para que los demas tambien lo puedan ver. | Debe | 2 Días | Se probara viendo que el sensor mande la informacion correcta a la pantalla de acuerdo al pulso del usuario. | Israel |

### Prototipo propuesto por el equipo para el proyecto
![](https://github.com/Anthonyy12/wearable/blob/main/images/PrototipoEnDibujo.jpg)
# En Fisico
![](https://github.com/Anthonyy12/wearable/blob/main/images/protoFisico.jpg)

### Despliegue del Dashboard
![]()

### Comunicación MQTT
![]()

### Base de Datos
![]()

### Carta de Agradecimiento
![]()
