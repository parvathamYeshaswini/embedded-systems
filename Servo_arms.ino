#include <PRIZM.h>
PRIZM prizm;

// ---- ARM SERVO DEFINES ----
#define ARM_L_PIN 3   // digital pin 3 for left arm
#define ARM_R_PIN 2   // digital pin 2 for right arm
#define ARM_L_MIN 90  // min degree for left arm
#define ARM_L_MAX 130 // max degree for left arm
#define ARM_R_MIN 40  // min degree for right arm
#define ARM_R_MAX 90  // max degree for right arm

// ---- DRIVE MOTOR PORTS (CHANGE IF NEEDED) ----
#define LEFT_MOTOR  1   // motor M1
#define RIGHT_MOTOR 2   // motor M2

// ---------- ARM CONTROL ----------
void arm_grab() {
  prizm.setServoPosition(ARM_L_PIN, ARM_L_MAX);
  prizm.setServoPosition(ARM_R_PIN, ARM_R_MIN);
}

void arm_release() {
  prizm.setServoPosition(ARM_L_PIN, ARM_L_MIN);
  prizm.setServoPosition(ARM_R_PIN, ARM_R_MAX);
}

// ---------- DRIVE CONTROL ----------
void stop_drive() {
  prizm.setMotorPower(LEFT_MOTOR, 0);
  prizm.setMotorPower(RIGHT_MOTOR, 0);
}

// straight forward
void drive_forward(int power) {
  prizm.setMotorPower(LEFT_MOTOR, power);
  prizm.setMotorPower(RIGHT_MOTOR, power);
}

// spin in place to the right
void spin_right(int power) {
  prizm.setMotorPower(LEFT_MOTOR, power);
  prizm.setMotorPower(RIGHT_MOTOR, -power);
}

// ---------- SETUP (single one!) ----------
void setup() {
  prizm.PrizmBegin();          // initialize PRIZM

  prizm.setServoSpeed(1, 25);  // adjust channel numbers if needed
  prizm.setServoSpeed(2, 25);

  arm_release();               // start with arm open
  stop_drive();

  Serial.begin(115200);        // for commands from Raspberry Pi
}

// ---------- LOOP ----------
void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();   // ✅ no argument

    switch (cmd) {
      case 'F':   // forward
        drive_forward(60);
        break;

      case 'R':   // rotate/search
        spin_right(40);
        break;

      case 'S':   //
