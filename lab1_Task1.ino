#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;

void setup() {
  prizm.PrizmBegin();
}

void loop() {
  prizm.setMotorPowers(-30,30);      // go forward at 50% power
  delay(2000);                      // wait here for .6 seconds while motors spin
 // prizm.setMotorPowers(125,125);    // stop both motors with in brake mode
  //delay(1000);
  prizm.setMotorPowers(48,48);     // make a right turn
  delay(600);   // 
}
  
