/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/

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
  
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,256)) + ',');
  Serial.print(String(random(0,256)) + ',');
  Serial.print(String(random(256,512)) + ',');
  Serial.print(String(random(256,512)) + ',');
  Serial.print(String(random(512,768)) + ',');
  Serial.print(String(random(512,768)) + ',');
  Serial.print(String(random(768,1023)) + ',');
  Serial.print(String(random(768,1023)) + ',');
  Serial.print(String(random(512,768)) + ',');
  Serial.print(String(random(512,768)) + ',');
  Serial.print(String(random(256,512)) + ',');
  Serial.print(String(random(256,512)) + ',');
  Serial.print(String(random(0,256)) + ',');
  Serial.print(String(random(0,256)) + ',');
  Serial.println(String(random(0,128)));
  delay(1);
  /*
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.print(String(random(0,128)) +  ',');
  Serial.println(String(random(0,128)));
  delay(1);

  */
    // delay in between reads for stability
}
