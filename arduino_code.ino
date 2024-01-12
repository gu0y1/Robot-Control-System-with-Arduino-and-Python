#include <Arduino.h>

char lastCommand = 'n'; // 初始命令设置为'n'
unsigned long previousMillis = 0;

const long interval = 200; // 设定发送间隔为0.2秒
const int trigPin = 9;     // Trig 引脚连接到数字引脚 9
const int echoPin = 10;    // Echo 引脚连接到数字引脚 10
float radius = 2.0;        // 马达轮子半径（假设单位）
int lastEncoder_l = 0;     // 左侧编码器上一次读数
int lastEncoder_r = 0;     // 右侧编码器上一次读数
float lastLinearSpeed = 0.0; // 上一次的线速度

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT); // 将 Trig 引脚设置为输出
  pinMode(echoPin, INPUT);  // 将 Echo 引脚设置为输入
  lastEncoder_l = analogRead(A0); // 初始化编码器读数
  lastEncoder_r = analogRead(A1);
}

void loop() {
  unsigned long currentMillis = millis();

  if (Serial.available() > 0) {
    lastCommand = Serial.read();
    executeCommand(lastCommand);
  }

  if (currentMillis - previousMillis >= interval) {
    sendResponse();
    previousMillis = currentMillis;
  }
}

float calculateDistance() {
  float totalDistance = 0;
  int numMeasurements = 5;  // 测量次数
  for (int i = 0; i < numMeasurements; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH, 20000);  // 20毫秒超时
    if(duration > 0) {
      totalDistance += duration * 0.034 / 2;
    }
    delay(10); // 间隔一段时间再进行下一次测量
  }
  return totalDistance / numMeasurements; // 返回平均值
}


void executeCommand(char command) {
  // ... 其他指令处理 ...
}

float calculateSpeed(int &lastEncoder, int currentEncoder) {
  int delta = currentEncoder - lastEncoder; // 计算编码器变化量
  lastEncoder = currentEncoder; // 更新编码器读数
  return delta * radius * 1000.0 / interval; // 速度 = 变化量 x 半径 x 时间因子
}

void sendResponse() {
  int currentEncoder_l = analogRead(A0);
  int currentEncoder_r = analogRead(A1);
  
  float speed_l = calculateSpeed(lastEncoder_l, currentEncoder_l);
  float speed_r = calculateSpeed(lastEncoder_r, currentEncoder_r);
  float v_linear_ICR = (speed_l + speed_r) / 2.0; // 线速度为两轮速度的平均值
  float v_angular_ICR = speed_r - speed_l; // 角速度为两轮速度差
  float acceleration = (v_linear_ICR - lastLinearSpeed) / (interval / 1000.0); // 加速度
  float distance = calculateDistance();
  lastLinearSpeed = v_linear_ICR;

  int checksum = ((int)v_linear_ICR + (int)acceleration + (int)v_angular_ICR) % 2;

  Serial.print(lastCommand);
  Serial.print(",");
  Serial.print(speed_l, 2); // 保留两位小数
  Serial.print(",");
  Serial.print(speed_r, 2); // 保留两位小数
  Serial.print(",");
  Serial.print(v_linear_ICR, 2); // 保留两位小数
  Serial.print(",");
  Serial.print(acceleration, 2); // 保留两位小数
  Serial.print(",");
  Serial.print(v_angular_ICR, 2); // 保留两位小数
  Serial.print(",");
  Serial.print(distance, 2);
  Serial.print(",");
  Serial.println(checksum);
}
