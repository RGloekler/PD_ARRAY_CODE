// REFERENCES: 
// adapted from https://stackoverflow.com/questions/28887617/arduino-fill-array-with-values-from-analogread
// https://forum.arduino.cc/t/use-external-trigger-to-start-the-timer/567070/3
// https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/

// Ryan Gloekler, UC Davis. Hunt Vacuum Microectronics Lab
// regloekler@ucdavis.edu
// Takes an input trigger from DG535, which causes an interrupt. 100 data samples are taken at 10KHz
// (10 ms total sampling time). Data is then sent to serial, where it can be retrieved by python for processing.
// Last edit: 2/29/2024

// storing 100 values @ 10KHz = 10ms of data. Solenoid should be active ~5ms.
const unsigned int readings  = 100;
const unsigned int numPixels = 16;
unsigned int analogVals[readings][numPixels]; // create an array to store data readings in 
unsigned int i = 0;

const int INTERRUPT_PIN = 2;
volatile int triggeredFLAG = 0; // initially set interrupt flag to low..

void setup()
{
  pinMode(INTERRUPT_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), collectSamples, RISING);
  Serial.begin(115200);
}

void loop()
{  
  static uint32_t tStart = micros(); // grab start time
  const uint32_t period = 100; // setting measurement frequency to 10KHz
  uint32_t tNow = micros(); 

  if (tNow - tStart >= period && triggeredFLAG) // check to see if collection is active and interrupt is recieved
  {
    tStart += period; // update start time to ensure consistent and near-exact period

    // TAKE DATA FROM PIXELS
    analogVals[i][0] = analogRead(A0);
    analogVals[i][1] = analogRead(A1);
    analogVals[i][2] = analogRead(A2);
    analogVals[i][3] = analogRead(A3);
    analogVals[i][4] = analogRead(A4);
    analogVals[i][5] = analogRead(A5);
    analogVals[i][6] = analogRead(A6);
    analogVals[i][7] = analogRead(A7);
    analogVals[i][8] = analogRead(A8);
    analogVals[i][9] = analogRead(A9);
    analogVals[i][10] = analogRead(A10);
    analogVals[i][11] = analogRead(A11);
    analogVals[i][12] = analogRead(A12);
    analogVals[i][13] = analogRead(A13);
    analogVals[i][14] = analogRead(A14);
    analogVals[i][15] = analogRead(A15);
   
    i++; // increment data counter value for analogVals
    
    if (i>=readings) {
      int counter = 0;
      Serial.println("Captured Data, exiting");
      for (int x = 0; x < 100; x++) {
        for (int y = 0; y <= 15; y++) {
          Serial.print(analogVals[x][y]);
          Serial.print(", ");
        }
        Serial.println("Sample: " + String(counter));
        counter++;
      }
      delay(1000); // wait one second for stabilization, then become available for interrupts agains
      triggeredFLAG = 0;
      i = 0; //reset to beginning of array, so other readings overwrite existing data
    }
  }
}

// interrupt sets triggeredFLAG to high, which allows data collection to begin
void collectSamples(){
  triggeredFLAG = 1;
}
