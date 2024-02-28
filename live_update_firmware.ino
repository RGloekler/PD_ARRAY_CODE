// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  int sensorValue1 = analogRead(A1);
  int sensorValue2 = analogRead(A2);
  int sensorValue3 = analogRead(A3);
  int sensorValue4 = analogRead(A4);
  int sensorValue5 = analogRead(A5);
  int sensorValue6 = analogRead(A6);
  int sensorValue7 = analogRead(A7);
  int sensorValue8 = analogRead(A8);
  int sensorValue9 = analogRead(A9);
  int sensorValue10 = analogRead(A10);
  int sensorValue11 = analogRead(A11);
  int sensorValue12 = analogRead(A12);
  int sensorValue13 = analogRead(A13);
  int sensorValue14 = analogRead(A14);
  int sensorValue15 = analogRead(A15);
  
  
  // print out the value you read:  
  Serial.print(String(sensorValue) + ',');
  Serial.print(String(sensorValue1) + ',');
  Serial.print(String(sensorValue2) + ',');
  Serial.print(String(sensorValue3) + ',');
  Serial.print(String(sensorValue4) + ',');
  Serial.print(String(sensorValue5) + ',');
  Serial.print(String(sensorValue6) + ',');
  Serial.print(String(sensorValue7) + ',');
  Serial.print(String(sensorValue8) + ',');
  Serial.print(String(sensorValue9) + ',');
  Serial.print(String(sensorValue10) + ',');
  Serial.print(String(sensorValue11) + ',');
  Serial.print(String(sensorValue12) + ',');
  Serial.print(String(sensorValue13) + ',');
  Serial.print(String(sensorValue14) + ',');
  Serial.println(String(sensorValue15));
  delay(175);

}
