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
| 1  | Thonny | 4.1.6 | Open Source |
| 2  | Visual Studio Code | 1.92.2  | Open Source |
| 3  | Firebase | -  | Freemium |
| 4  | Flutter | 3.22.2  | Open Source |


### Hardware empleado
| ID  | Nombre                      | Descripción                                                                                                                              | Imagen | Costo Unitario | Cantidad |
|-----|-----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------:|--------|:--------------:|:--------:|
| 1   | ESP32                       | La ESP32 actuaría como el cerebro de la gorra inteligente, gestionando la conectividad, procesando los datos de los sensores y controlando la interacción con otros dispositivos para brindar una experiencia adaptada a las necesidades de las personas sordas. |  ![esp](https://github.com/Anthonyy12/wearable/blob/main/images/esp.jpg)      | $300           | 1        |
| 2   | HC-SR04                     | Puede detectar la presencia de objetos cercanos. Esto podría ser útil para alertar a la persona sorda sobre la presencia de obstáculos o personas cercanas, evitando posibles colisiones. |    ![hc](https://github.com/Anthonyy12/wearable/blob/main/images/hc.jpg)    | $50            | 1        |
| 3   | MPU6050                     | Sensor acelerómetro y giroscopio que puede detectar el movimiento y la orientación. Esto podría ayudar a la gorra inteligente a detectar el movimiento del usuario y proporcionar retroalimentación relevante. |   ![mpu](https://github.com/Anthonyy12/wearable/blob/main/images/mpu6050.jpg)     | $74           | 1        |
| 4   | Pantalla OLED 0.96"         | Pantalla de visualización para mostrar información al usuario, como el estado del dispositivo o alertas importantes. |   ![oled](https://github.com/Anthonyy12/wearable/blob/main/images/oled.jpg)     | $283           | 1        |
| 5   | Buzzer pasivo ARD-356        | Puede emitir sonidos como alertas auditivas para el usuario. Podría ser útil para notificaciones. |  ![buzzerpas](https://github.com/Anthonyy12/wearable/blob/main/images/buzzerpasivo.jpg)      | $29            | 1        |
| 6   | Buzzer                      | Similar al buzzer pasivo, puede emitir sonidos para notificaciones o alertas. |   ![buzzer](https://github.com/Anthonyy12/wearable/blob/main/images/buzzer.jpg)     | $15            | 1        |
| 7  | LED RGB                     | LED que emite luz de diferentes colores (Rojo, Verde, Azul), útil para indicar diferentes estados o alertas visuales. |   ![rgb](https://github.com/Anthonyy12/wearable/blob/main/images/rgb.jpg)     | $10            | 1        |
| 8  | LED  Amarillo                   | LED que emite luz útil para indicar diferentes estados o alertas visuales. |      ![led](https://github.com/user-attachments/assets/37cf9624-53c1-4822-8951-e38984c6d418)| $10       | 1     |
| 8  | LDR(Fotorresistencia)                   | Util para indicar el nivel de luz |   ![LDR](https://github.com/user-attachments/assets/ec7a472a-478f-49e6-b402-0d3bb7d119e6)| $10       | 1     |
| 9  | Resistencias de 330 ohmios y 2k ohmios | Componentes necesarios para regular la corriente y proteger los componentes electrónicos. |   ![resistencias](https://github.com/Anthonyy12/wearable/blob/main/images/330.jpg)     | $1             | 2        |
| 10  | Cables jumper dupont         | Cables para realizar conexiones entre los diferentes componentes en el protoboard o circuito. |  ![jumpers](https://github.com/Anthonyy12/wearable/blob/main/images/jumpers.jpg)      | $117            | 10       |
| 11  | Regulador                   | Componente que regula el voltaje para mantener una alimentación estable para los componentes. |     ![reguladordevoltios](https://github.com/user-attachments/assets/c9f9fd79-2dc3-4f73-a143-493b5a1f021c)| $120            | 1        |
| 12  | Placa fenolica           | Utilizado para conectar los componentes electrónicos durante el desarrollo y pruebas del circuito. |     ![placafenolica](https://github.com/user-attachments/assets/87df3366-5011-4820-b605-d70829fe9aa0)| $90            | 1        |
| 12  | Estaño           | Utilizado para reducir el numero de cables y hacer conexion entre la esp32 y los componentes |  ![unnamed](https://github.com/user-attachments/assets/e155ef3a-6310-44cf-abf6-8dce2274df12)| $90            | 1        |
| 13  | Sensor MQ-2           | Utilizado para detectar distintos tipos de gases, como metano, hetano, etc | ![mq2](https://github.com/user-attachments/assets/f776b1b3-d1c3-416c-91d3-6741da16f556)| $150            | 1        |



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
![Imagen de WhatsApp 2024-11-01 a las 21 15 39_f84ad842](https://github.com/user-attachments/assets/54e57ae1-6f90-41d8-a29d-bcba5874037a)
![Imagen de WhatsApp 2024-11-01 a las 21 15 39_599cace5](https://github.com/user-attachments/assets/6ab129a0-898f-4da0-9e2c-9002ca1d9845)
![Imagen de WhatsApp 2024-11-01 a las 21 15 39_198f989d](https://github.com/user-attachments/assets/42297539-2637-4489-80cd-164701308e05)

### Despliegue del Dashboard
![Imagen de WhatsApp 2024-11-01 a las 21 16 10_9be867d0](https://github.com/user-attachments/assets/46dc9f59-8c54-4fce-bc0f-029bdfa07a14)
![Imagen de WhatsApp 2024-11-01 a las 21 16 48_ca8c312b](https://github.com/user-attachments/assets/b1d6b853-fe0a-4ef5-9a29-412178b9495d)
![Imagen de WhatsApp 2024-11-03 a las 21 41 32_c32790d3](https://github.com/user-attachments/assets/5e245a6d-12b7-45f7-b87e-16629fef0172)
![Imagen de WhatsApp 2024-11-03 a las 21 41 52_dba18d74](https://github.com/user-attachments/assets/ef5a6274-ce47-4f1c-9e56-7919761f50ba)

### Comunicación MQTT
![Imagen de WhatsApp 2024-11-03 a las 21 31 31_241bb0be](https://github.com/user-attachments/assets/61356f7e-6443-431e-b00a-35a3cf2887b6)
![Imagen de WhatsApp 2024-11-03 a las 21 31 46_7dafda60](https://github.com/user-attachments/assets/4bbb209e-22df-4f13-a0cb-54bb708ab3da)

### Base de Datos
![Imagen de WhatsApp 2024-11-03 a las 21 13 11_66f93f19](https://github.com/user-attachments/assets/b3ce153d-9cc8-49f1-bebf-db5da626627a)

### Video
Presione la imagen para ver el video

[![Mira el video](https://img.youtube.com/vi/83fRAsLHXcg/0.jpg)](https://www.youtube.com/watch?v=83fRAsLHXcg)

### Carta de Agradecimiento
![Imagen de WhatsApp 2024-11-03 a las 21 27 39_56050b01](https://github.com/user-attachments/assets/e6e8fea8-7a08-4574-9acd-9baa40419675)

