/*
  PCB Oven controller

  Phase 0    0 --> 150  Warm up
  Phase 1  150 --> 180  Soak
  phase 2  220 --> 245  Ramp up
  Phase 3  250 (25 sec) Peak
  phase 4  250 --> 217  Cool
  Phase 5  217 -->  25  Finish

  This script uses AutoPID library by rdownin4 under MIT license.
*/
#include "AutoPID.h"
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
#define Kp 0.1
#define Ki 0
#define Kd 10

double temperature;
double setPoint;
bool relayState;
double pulseWidth = 2000; // in miliseconds
double timeStep = 2000;   // how often the PID should update in miliseconds
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
    if (temperature < 148) {
      return 150;
    } else {
      startNewPhase(1);
    }
  }
  if (currentPhase == 1) {
    // preheat area (should last 90 seconds)
    if (secondsInPhase < 90) {
      return 150 + 30 * secondsInPhase / 90;
    } else {
      startNewPhase(2);
    }
  }
  if (currentPhase == 2) {
    // go to peak area (at max 3 deg /s)
    if (temperature < 243) {
      return min(245, 180 + 2 * secondsInPhase);
    } else {
      startNewPhase(3);
      // turn off secondary heater
      digitalWrite(PIN_SECOND, false);
    }
  }
  if (currentPhase == 3) {
    // stay in peak area
    if (secondsInPhase < 25) {
      return 249;
    } else {
      startNewPhase(4);
    }
  }
  if (currentPhase == 4) {
    // decend to beneath peak (at max -6 deg /s, best is -2 deg /s)
    if (temperature > 150) {
      return max(25, 250 - 2 * secondsInPhase);
    } else {
      startNewPhase(5);
    }
  }
  if (currentPhase == 5) {
    // Finish by going to room temperature
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
  lcd.begin(16, 2);
  lcd.clear();
  pinMode(PIN_MAIN, OUTPUT);
  pinMode(PIN_SECOND, OUTPUT);
  pinMode(PIN_SENSOR, INPUT);
  //set PID update interval
  myPID.setTimeStep(timeStep);
  startNewPhase(0);
  // fire up secondary heater
  digitalWrite(PIN_SECOND, true);
}


void setLcd() {
  if ((timeCurrent - timeLcdUpdate) > 500) {
    timeLcdUpdate = timeCurrent;
    lcd.clear();
    lcd.setCursor(0, 0);
    if (currentPhase == 0) {
      lcd.print("0 Warm up");
    } else if (currentPhase == 1) {
      lcd.print("1 Soak");
    } else if (currentPhase == 2) {
      lcd.print("2 Ramp up");
    } else if (currentPhase == 3) {
      lcd.print("3 Peak");
    } else if (currentPhase == 4) {
      lcd.print("4 OPEN THE DOOR");
    } else if (currentPhase == 5) {
      lcd.print("5 OPEN THE DOOR");
    } 
    if (currentPhase < 4) {
      lcd.setCursor(11, 0);
      lcd.print((int) secondsInPhase);
    }
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

