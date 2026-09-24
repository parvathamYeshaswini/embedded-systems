#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;

void setup() {
  prizm.PrizmBegin();
}

void loop() {
  if (prizm.readSonicSensorCM(3)>20){
    prizm.setMotorPowers(-30,30);      // go forward at 50% power
 // delay(2000); 
  }
  else if (prizm.readSonicSensorCM(3) < 10){
    prizm.setMotorPowers(30,-30);
  }
  else {
    prizm.setMotorPowers(125, 125);
  }
}
