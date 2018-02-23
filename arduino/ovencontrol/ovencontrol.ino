/*
  PCB Oven controller

  Phase 0    0 --> 150
  Phase 1  150 --> 180
  Phase 2  180 --> 220
  phase 3  220 --> 245
  Phase 4  250
  phase 5  250 --> 217
  Phase 6  217 -->  25

*/
#include <AutoPID.h>
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//pins
#define PIN_MAIN 8
#define PIN_SECOND 7
#define PIN_SENSOR A5

//pid settings and gains
#define Kp 0.2
#define Ki 0
#define Kd 2

double temperature;
double setPoint;
bool relayState;
double pulseWidth = 2000; // in miliseconds
double timeStep = 5000;   // how often the PID should update in miliseconds
unsigned long timePhaseStart;
unsigned long timeCurrent;
unsigned long timeLcdUpdate;
unsigned long timeSerialUpdate;
int secondsInPhase;
int currentPhase;


//input/output variables passed by reference, so they are updated automatically
// AutoPIDRelay(double *input, double *setpoint, bool *relayState,
//              double pulseWidth, double Kp, double Ki, double Kd)
AutoPIDRelay myPID(&temperature, &setPoint, &relayState, pulseWidth, Kp, Ki, Kd);


double getTemperature() {
  // https://www.adafruit.com/product/1778
  int value = analogRead(PIN_SENSOR);  // 0 -- 1023
  return ((5 * (double) value / 1024) - 1.25) / 0.005;
}


double getSetPoint() {
  secondsInPhase = (timeCurrent - timePhaseStart) / 1000;
  if (currentPhase == 0) {
    // go to preheat start temperature
    if (temperature >= 150 * 0.95) {
      startNewPhase(1);
    } else {
      return 150;
    }
  }
  if (currentPhase == 1) {
    // preheat area
    double phaseDuration = 90;
    if (secondsInPhase >= phaseDuration) {
      startNewPhase(2);
    } else {
      if (secondsInPhase > 60) {
        digitalWrite(PIN_SECOND, true);
      }
      return 150 + 30 * secondsInPhase / phaseDuration;
    }
  }
  if (currentPhase == 2) {
    // go to lower peak area
    if (temperature >= 220 * 0.95) {
      digitalWrite(PIN_SECOND, false);
      startNewPhase(3);
    } else {
      digitalWrite(PIN_SECOND, true);
      return 220;
    }
  }
  if (currentPhase == 3) {
    // go to peak area
    if (temperature >= 245 * 0.95) {
      startNewPhase(4);
    } else {
      // max rate of 3 deg /s
      return 217 + 2 * (secondsInPhase);
    }
  }
  if (currentPhase == 4) {
    // stay in peak area
    if (secondsInPhase >= 25) {
      startNewPhase(5);
    } else {
      return 250;
    }
  }
  if (currentPhase == 5) {
    // slowly decend to beneath peak
    if (temperature < 217) {
      startNewPhase(6);
    } else {
      // max rate of -6 deg /s
      return 250 - 5 * (secondsInPhase);
    }
  }
  if (currentPhase == 6) {
    // cool down
    return 25;
  }
}


void startNewPhase(int phase) {
  currentPhase = phase;
  timePhaseStart = timeCurrent;
  secondsInPhase = 0;
}


void setup() {
  Serial.begin(9600);
  pinMode(PIN_MAIN, OUTPUT);
  pinMode(PIN_SECOND, OUTPUT);
  pinMode(PIN_SENSOR, INPUT);
  //if temperature is more than 50 degrees below or above setpoint, OUTPUT will be set to min or max respectively
  myPID.setBangBang(50);
  //set PID update interval
  myPID.setTimeStep(timeStep);
  startNewPhase(0);
  lcd.begin(16, 2);
  lcd.clear();
}


void setLcd() {
  if ((timeCurrent - timeLcdUpdate) > 500) {
    timeLcdUpdate = timeCurrent;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Phase ");
    lcd.print(currentPhase);
    lcd.setCursor(10, 0);
    lcd.print((int) secondsInPhase);
    lcd.setCursor(0, 1);
    lcd.print((int) setPoint);
    lcd.print((char) 223);
    lcd.print("C");
    lcd.setCursor(9, 1);
    lcd.print((int) temperature);
    lcd.print((char) 223);
    lcd.print("C");
  }
}

void serialPrint() {
  if ((timeCurrent - timeSerialUpdate) > 1000) {
    timeSerialUpdate = timeCurrent;
    Serial.print(currentPhase);
    Serial.print(',');
    Serial.print(secondsInPhase);
    Serial.print(',');
    Serial.print(setPoint);
    Serial.print(',');
    Serial.print(temperature);
    Serial.print(',');
    Serial.println(myPID.getPulseValue());
  }
}

void loop() {
  timeCurrent = millis();
  temperature = getTemperature();
  setPoint = getSetPoint();
  myPID.run(); //call every loop, updates automatically at certain time interval
  digitalWrite(PIN_MAIN, relayState);
  setLcd();
  serialPrint();
}

