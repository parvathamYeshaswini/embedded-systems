#include <PRIZM.h>
#include <Wire.h>
PRIZM prizm;

void setup() {
  prizm.PrizmBegin();
}

void loop() {
 
  while (prizm.readSonicSensorCM(3)>40){
    prizm.setMotorPowers(-15,15);
 
  }
  Serial.print(prizm.readSonicSensorCM(3));   // print the CM distance to the serial monitor

  Serial.println(" Centimeters\n");             // print " Centimeters"

  delay(200); 
  prizm.setMotorPowers(125,125); 
  delay(800);
   prizm.setMotorPowers(15,15);     // make a 180 right turn (works do not touch)
  delay(2850);
 
  prizm.setMotorPowers(125,125); 
  delay(1000);
  
  float distance = prizm.readSonicSensorCM(3) + 40;
  while ( prizm.readSonicSensorCM(3) > (distance/2)){
    prizm.setMotorPowers(-15,15); 
    
  
  } 
  prizm.setMotorPowers(125,125); 
   delay(1000);
  
   prizm.setMotorPowers(15,15);     // make a 90 right turn (works do not touch)
  delay(1480);
 
  //seconf half
    while (prizm.readSonicSensorCM(3)>40){
    prizm.setMotorPowers(-15,15);
 
  }
  Serial.print(prizm.readSonicSensorCM(3));   // print the CM distance to the serial monitor

  Serial.println(" Centimeters\n");             // print " Centimeters"

  delay(200); 
  prizm.setMotorPowers(125,125); 
  delay(800);
   prizm.setMotorPowers(15,15);     // make a 180 right turn (works do not touch)
  delay(2850);
 
  prizm.setMotorPowers(125,125); 
  delay(1000);
  
  float distance1 = prizm.readSonicSensorCM(3) + 40;
  while ( prizm.readSonicSensorCM(3) > (distance1/2)){
    prizm.setMotorPowers(-15,15); 
    
  
  } 
  prizm.setMotorPowers(125,125); 
   delay(1000);
  
   prizm.setMotorPowers(15,15);     // make a 90 right turn (works do not touch)
  delay(1480);
  
  
  prizm.PrizmEnd(); 
}
