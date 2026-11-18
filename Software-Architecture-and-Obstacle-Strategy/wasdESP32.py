#include <ESP32Servo.h>

// Motor driver pins
#define IN1 25
#define IN2 26
#define ENA 27

// Servo
const int servoPin = 18;
const int SERVO_MIN = 30;
const int SERVO_MAX = 160;
const int SERVO_STEP_MS = 10;     // time per 1-degree step (lower = faster)

// Motor PWM
const int pwmFreq = 1000;
const int pwmRes = 8;             // 0-255
const int MAX_SPEED = 255;
const unsigned long TIMEOUT_MS = 200;

Servo myServo;
int servoAngle = 90;
char motorCmd = 'X';
char servoCmd = 'N';
unsigned long lastCmdTime = 0;
unsigned long lastServoStep = 0;

#if ESP_ARDUINO_VERSION_MAJOR >= 3
  void setupPWM() { ledcAttach(ENA, pwmFreq, pwmRes); }
  void setSpeed(int speed) { ledcWrite(ENA, speed); }
#else
  const int pwmChannel = 15;      // high channel so it doesn't clash with the servo
  void setupPWM() {
    ledcSetup(pwmChannel, pwmFreq, pwmRes);
    ledcAttachPin(ENA, pwmChannel);
  }
  void setSpeed(int speed) { ledcWrite(pwmChannel, speed); }
#endif

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  setSpeed(MAX_SPEED);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  setSpeed(MAX_SPEED);
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  setSpeed(0);
}

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  setupPWM();
  stopMotor();

  ESP32PWM::allocateTimer(0);
  myServo.setPeriodHertz(50);
  myServo.attach(servoPin, 500, 2400);
  myServo.write(servoAngle);
}

void loop() {
  // Read commands: W/S/X for the motor, A/D/N for the servo
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'W' || c == 'S' || c == 'X') {
      motorCmd = c;
      lastCmdTime = millis();
    } else if (c == 'A' || c == 'D' || c == 'N') {
      servoCmd = c;
      lastCmdTime = millis();
    }
  }

  // Safety: no commands -> stop motor and freeze servo
  if (millis() - lastCmdTime > TIMEOUT_MS) {
    motorCmd = 'X';
    servoCmd = 'N';
  }

  // Motor
  if (motorCmd == 'W') forward();
  else if (motorCmd == 'S') backward();
  else stopMotor();

  // Servo: move 1 degree at a time, limited to 60-120
  if (servoCmd != 'N' && millis() - lastServoStep >= SERVO_STEP_MS) {
    lastServoStep = millis();
    if (servoCmd == 'D') servoAngle--;
    if (servoCmd == 'A') servoAngle++;
    servoAngle = constrain(servoAngle, SERVO_MIN, SERVO_MAX);
    myServo.write(servoAngle);
  }
}