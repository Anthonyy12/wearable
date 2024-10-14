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
      title: 'Ultrasonic Sensor MQTT',
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
  final String topicMPU = 'sensores/acelerometro'; // Tópico para datos MPU

  MqttServerClient? client;
  String sensorData = '';
  List<ChartData> distanceData = [];
  List<ChartData> lightData = []; // Lista para almacenar datos de luz
  List<PolarChartData> mpuData = []; // Lista para datos de MPU
  double lightValue = 0; // Valor de luz
  int selectedGraph =
      0; // 0 para gráfica de distancia, 1 para gauge de luz, 2 para line chart MPU, 3 para todas las gráficas juntas
  bool isConnecting = false; // Para evitar múltiples intentos de conexión

  @override
  void initState() {
    super.initState();
    connectMQTT();
  }

  void connectMQTT() async {
    if (isConnecting) return; // Evita múltiples reconexiones simultáneas
    isConnecting = true;

    client = MqttServerClient(broker, 'Lichita'); // ID único
    client!.port = 1883;
    client!.logging(on: true);
    client!.keepAlivePeriod = 60; // Mantener la conexión activa por más tiempo
    client!.connectTimeoutPeriod =
        5000; // Aumenta el tiempo de espera de la conexión

    client!.onConnected = onConnected;
    client!.onDisconnected = onDisconnected;
    client!.onSubscribed = onSubscribed;

    try {
      await client!.connect();
      print('Connected to MQTT broker');
    } catch (e) {
      print('Connection failed: $e');
      client!.disconnect();
      retryConnection(); // Intenta reconectar en caso de falla
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
      client = null; // Limpia la instancia del cliente
    }
  }

  void onConnected() {
    print('Connected');
    client!.subscribe(topicDistance, MqttQos.atLeastOnce);
    client!.subscribe(topicLight, MqttQos.atLeastOnce);
    client!
        .subscribe(topicMPU, MqttQos.atLeastOnce); // Subscribirse al tópico MPU
    print('Subscribed to topics: $topicDistance, $topicLight, $topicMPU');

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
      sensorData = 'Distance: $payload cm';
      updateChartData(distanceData, double.tryParse(payload) ?? 0, 0);
    } else if (topic == topicLight) {
      sensorData = 'Light: $payload';
      lightValue = double.tryParse(payload) ?? 0; // Actualiza el valor de luz
      updateChartData(lightData, lightValue, 1);
    } else if (topic == topicMPU) {
      sensorData = 'MPU: $payload';
      updateMPUData(payload); // Actualiza los datos de la gráfica line chart
    } else {
      print('Unknown topic: $topic'); // Para depuración
    }
  }

  void updateChartData(List<ChartData> chartData, double value, int type) {
    if (chartData.length > 20) {
      chartData.removeAt(0); // Remueve el primer punto si hay más de 20
    }
    chartData.add(ChartData(DateTime.now(), value));
  }

  void updateMPUData(String payload) {
    // Asume que los datos vienen en formato X,Y,Z separados por comas
    List<String> values = payload.split(',');
    if (values.length == 3) {
      double x = double.tryParse(values[0]) ?? 0;
      double y = double.tryParse(values[1]) ?? 0;
      double z = double.tryParse(values[2]) ?? 0;

      if (mpuData.length > 20) {
        mpuData.removeAt(0);
      }

      // Almacena la fecha y hora de recepción junto con los valores de X, Y, Z
      mpuData.add(PolarChartData(DateTime.now(), x, y, z));
    }
  }

  void onDisconnected() {
    print('Disconnected');
    retryConnection(); // Intenta reconectar cuando se desconecta
  }

  void onSubscribed(String topic) {
    print('Subscribed to $topic');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ultrasonic Sensor MQTT'),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment(0.8, 1),
            colors: <Color>[
              Color.fromARGB(255, 87, 80, 100),
              Color.fromARGB(255, 103, 93, 104),
              Color.fromARGB(255, 112, 104, 110),
              Color.fromARGB(255, 131, 123, 126),
              Color.fromARGB(255, 146, 138, 139),
              Color.fromARGB(255, 148, 143, 143),
              Color.fromARGB(255, 177, 174, 173),
              Color.fromARGB(255, 228, 226, 225),
            ],
            tileMode: TileMode.mirror,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Botones para elegir el gráfico
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
                      selectedGraph = 3; // Mostrar las tres gráficas juntas
                    });
                  },
                  child: const Text('Ver todas las gráficas'),
                ),
              ],
            ),
            const SizedBox(
                height: 20), // Espacio entre los botones y el gráfico
            Expanded(
              child: selectedGraph == 0
                  ? buildDistanceChart()
                  : selectedGraph == 1
                      ? buildLightGauge()
                      : selectedGraph == 2
                          ? buildLineChart()
                          : buildAllCharts(), // Mostrar todas las gráficas juntas
            ),
            // Mostrar datos solo del sensor correspondiente
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                selectedGraph == 0
                    ? (distanceData.isEmpty
                        ? 'No distance data received'
                        : 'Distance: ${distanceData.last.value} cm')
                    : selectedGraph == 1
                        ? (lightData.isEmpty
                            ? 'No light data received'
                            : 'Light: ${lightData.last.value}')
                        : selectedGraph == 2
                            ? (mpuData.isEmpty
                                ? 'No MPU data received'
                                : 'MPU: X=${mpuData.last.x}, Y=${mpuData.last.y}, Z=${mpuData.last.z}')
                            : 'Mostrando todas las gráficas',
                style: const TextStyle(fontSize: 24, color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildAllCharts() {
    return Column(
      children: [
        Expanded(child: buildDistanceChart()),
        const SizedBox(height: 20),
        Expanded(child: buildLightGauge()),
        const SizedBox(height: 20),
        Expanded(child: buildLineChart()),
      ],
    );
  }

  Widget buildDistanceChart() {
    return SfCartesianChart(
      title: ChartTitle(text: 'Distance Sensor'),
      primaryXAxis: DateTimeAxis(),
      series: <LineSeries<ChartData, DateTime>>[
        LineSeries<ChartData, DateTime>(
          dataSource: distanceData, // Datos solo de distancia
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
          maximum: 600, // Ajusta según el rango de tu sensor de luz
          pointers: <GaugePointer>[
            NeedlePointer(value: lightValue), // Usa el valor actualizado de luz
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
      primaryXAxis: DateTimeAxis(
        title: AxisTitle(text: 'Time'),
      ),
      primaryYAxis: NumericAxis(
        title: AxisTitle(text: 'Value'),
      ),
      legend: Legend(isVisible: true), // Mostrar leyenda para identificar ejes
      tooltipBehavior: TooltipBehavior(enable: true), // Habilitar tooltips
      series: <LineSeries<PolarChartData, DateTime>>[
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.x,
          name: 'X Axis',
          color: Colors.red, // Color para el eje X
          markerSettings:
              const MarkerSettings(isVisible: true), // Marcadores visibles
        ),
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.y,
          name: 'Y Axis',
          color: Colors.green, // Color para el eje Y
          markerSettings: const MarkerSettings(isVisible: true),
        ),
        LineSeries<PolarChartData, DateTime>(
          dataSource: mpuData,
          xValueMapper: (PolarChartData data, _) => data.time,
          yValueMapper: (PolarChartData data, _) => data.z,
          name: 'Z Axis',
          color: Colors.blue, // Color para el eje Z
          markerSettings: const MarkerSettings(isVisible: true),
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
