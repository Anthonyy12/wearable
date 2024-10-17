import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:syncfusion_flutter_gauges/gauges.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Control de Actuadores y Sensores',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const SensorPage(),
    );
  }
}

class SensorPage extends StatefulWidget {
  const SensorPage({super.key});

  @override
  _SensorPageState createState() => _SensorPageState();
}

class _SensorPageState extends State<SensorPage> {
  final String broker = 'broker.hivemq.com';
  final String topicDistance = 'sensores/distancia';
  final String topicLight = 'sensores/luz';
  final String topicMPU = 'sensores/acelerometro';
  final String topicMQ2 = 'sensores/mq2';

  MqttServerClient? client;
  String sensorData = '';
  List<ChartData> distanceData = [];
  List<ChartData> lightData = [];
  List<PolarChartData> mpuData = [];
  double lightValue = 0;
  double mq2Value = 0;
  double distanceValue = 0;
  String mpuValues = '';
  int selectedGraph = 0;
  bool isConnecting = false;

  @override
  void initState() {
    super.initState();
    connectMQTT();
  }

  void connectMQTT() async {
    if (isConnecting) return;
    isConnecting = true;

    client = MqttServerClient(broker, 'Lichita');
    client!.port = 1883;
    client!.logging(on: true);
    client!.keepAlivePeriod = 60;
    client!.connectTimeoutPeriod = 5000;

    client!.onConnected = onConnected;
    client!.onDisconnected = onDisconnected;

    try {
      await client!.connect();
      print('Connected to MQTT broker');
    } catch (e) {
      print('Connection failed: $e');
      client!.disconnect();
      retryConnection();
    } finally {
      isConnecting = false;
    }
  }

  void retryConnection() {
    Future.delayed(const Duration(seconds: 5), () {
      if (client!.connectionStatus?.state != MqttConnectionState.connected) {
        print('Retrying connection...');
        connectMQTT();
      }
    });
  }

  void disconnectMQTT() {
    if (client != null) {
      client!.disconnect();
      client = null;
    }
  }

  void onConnected() {
    print('Connected');
    client!.subscribe(topicDistance, MqttQos.atLeastOnce);
    client!.subscribe(topicLight, MqttQos.atLeastOnce);
    client!.subscribe(topicMPU, MqttQos.atLeastOnce);
    client!.subscribe(topicMQ2, MqttQos.atLeastOnce);

    client!.updates!.listen((List<MqttReceivedMessage<MqttMessage>> c) {
      final MqttPublishMessage message = c[0].payload as MqttPublishMessage;
      final payload =
          MqttPublishPayload.bytesToStringAsString(message.payload.message);
      print('Received message: $payload');
      setState(() {
        updateSensorData(c[0].topic, payload);
      });
    });
  }

  void updateSensorData(String topic, String payload) {
    if (topic == topicDistance) {
      distanceValue = double.tryParse(payload) ?? 0;
      updateChartData(distanceData, distanceValue, 0);
    } else if (topic == topicLight) {
      lightValue = double.tryParse(payload) ?? 0;
      updateChartData(lightData, lightValue, 1);
    } else if (topic == topicMPU) {
      updateMPUData(payload);
    } else if (topic == topicMQ2) {
      mq2Value = double.tryParse(payload) ?? 0;
    } else {
      print('Unknown topic: $topic');
    }
  }

  void updateChartData(List<ChartData> chartData, double value, int type) {
    if (chartData.length > 20) {
      chartData.removeAt(0);
    }
    chartData.add(ChartData(DateTime.now(), value));
  }

  void updateMPUData(String payload) {
    List<String> values = payload.split(',');
    if (values.length == 3) {
      double x = double.tryParse(values[0]) ?? 0;
      double y = double.tryParse(values[1]) ?? 0;
      double z = double.tryParse(values[2]) ?? 0;

      mpuValues =
          'X: $x, Y: $y, Z: $z'; // Actualiza los valores actuales de MPU

      if (mpuData.length > 20) {
        mpuData.removeAt(0);
      }
      mpuData.add(PolarChartData(DateTime.now(), x, y, z));
    }
  }

  void onDisconnected() {
    print('Disconnected');
    retryConnection();
  }

  void toggleActuator(String topic, String message) {
    if (client != null &&
        client!.connectionStatus?.state == MqttConnectionState.connected) {
      final builder = MqttClientPayloadBuilder();
      builder.addString(message);
      client!.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!);
      print('Sent $message to $topic');
    } else {
      print('Not connected');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Control de Actuadores y Sensores'),
      ),
      body: Column(
        children: [
          // Botones para seleccionar las gráficas
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    selectedGraph = 0; // Cambiar a gráfica de distancia
                  });
                },
                child: const Text('Gráfica de Distancia'),
              ),
              const SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    selectedGraph = 1; // Cambiar a gauge de luz
                  });
                },
                child: const Text('Gauge de Luz'),
              ),
              const SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    selectedGraph = 2; // Cambiar a gráfica de líneas (MPU)
                  });
                },
                child: const Text('Gráfica de Líneas MPU'),
              ),
              const SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    selectedGraph = 3; // Cambiar a gauge de MQ2
                  });
                },
                child: const Text('Gauge de MQ2'),
              ),
            ],
          ),
          // Botones de control para actuadores
          Expanded(
            flex: 2,
            child: Container(
              color: Colors.grey[200],
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/buzzer1', 'on');
                        },
                        child: const Text('Encender Buzzer 1'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/buzzer1', 'off');
                        },
                        child: const Text('Apagar Buzzer 1'),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/buzzer2', 'on');
                        },
                        child: const Text('Encender Buzzer 2'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/buzzer2', 'off');
                        },
                        child: const Text('Apagar Buzzer 2'),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/oled', 'on');
                        },
                        child: const Text('Encender OLED'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/oled', 'off');
                        },
                        child: const Text('Apagar OLED'),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/led_rgb', 'on');
                        },
                        child: const Text('Encender LED RGB'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/led_rgb', 'off');
                        },
                        child: const Text('Apagar LED RGB'),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/led', 'on');
                        },
                        child: const Text('Encender LED'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          toggleActuator('actuador/led', 'off');
                        },
                        child: const Text('Apagar LED'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          // Mostrar el valor del sensor correspondiente según la gráfica seleccionada
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text(
              selectedGraph == 0
                  ? 'Distancia: ${distanceValue.toStringAsFixed(2)} cm'
                  : selectedGraph == 1
                      ? 'Luz: ${lightValue.toStringAsFixed(2)}'
                      : selectedGraph == 2
                          ? 'MPU: $mpuValues'
                          : 'MQ2: ${mq2Value.toStringAsFixed(2)}',
              style: const TextStyle(fontSize: 20),
            ),
          ),
          // Gráficas
          Expanded(
            flex: 3,
            child: Container(
              padding: const EdgeInsets.all(8.0),
              color: Colors.grey[300],
              child: Column(
                children: [
                  Expanded(
                    child: selectedGraph == 0
                        ? buildDistanceChart()
                        : selectedGraph == 1
                            ? buildLightGauge()
                            : selectedGraph == 2
                                ? buildLineChart()
                                : buildMQ2Gauge(),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildDistanceChart() {
    return SfCartesianChart(
      title: ChartTitle(text: 'Distance Sensor'),
      primaryXAxis: DateTimeAxis(),
      primaryYAxis: NumericAxis(),
      series: <LineSeries<ChartData, DateTime>>[
        LineSeries<ChartData, DateTime>(
          dataSource: distanceData,
          xValueMapper: (ChartData data, _) => data.time,
          yValueMapper: (ChartData data, _) => data.value,
        ),
      ],
    );
  }

  Widget buildLightGauge() {
    return SfRadialGauge(
      title: const GaugeTitle(text: 'Light Intensity'),
      axes: <RadialAxis>[
        RadialAxis(
          minimum: 0,
          maximum: 600,
          pointers: <GaugePointer>[
            NeedlePointer(value: lightValue),
          ],
          ranges: <GaugeRange>[
            GaugeRange(startValue: 0, endValue: 200, color: Colors.green),
            GaugeRange(startValue: 200, endValue: 400, color: Colors.orange),
            GaugeRange(startValue: 400, endValue: 600, color: Colors.red),
          ],
        )
      ],
    );
  }

  Widget buildLineChart() {
    return SfCartesianChart(
      title: ChartTitle(text: 'MPU6050 Sensor Data'),
      primaryXAxis: DateTimeAxis(),
      primaryYAxis: NumericAxis(),
      series: <LineSeries<PolarChartData, DateTime>>[
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.x,
          name: 'X Axis',
        ),
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.y,
          name: 'Y Axis',
        ),
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.z,
          name: 'Z Axis',
        ),
      ],
    );
  }

  Widget buildMQ2Gauge() {
    return SfRadialGauge(
      title: const GaugeTitle(text: 'MQ2 Sensor'),
      axes: <RadialAxis>[
        RadialAxis(
          minimum: 0,
          maximum: 1000,
          pointers: <GaugePointer>[
            NeedlePointer(value: mq2Value),
          ],
          ranges: <GaugeRange>[
            GaugeRange(startValue: 0, endValue: 300, color: Colors.green),
            GaugeRange(startValue: 300, endValue: 700, color: Colors.orange),
            GaugeRange(startValue: 700, endValue: 1000, color: Colors.red),
          ],
        ),
      ],
    );
  }
}

class ChartData {
  ChartData(this.time, this.value);
  final DateTime time;
  final double value;
}

class PolarChartData {
  PolarChartData(this.time, this.x, this.y, this.z);
  final DateTime time;
  final double x;
  final double y;
  final double z;
}
