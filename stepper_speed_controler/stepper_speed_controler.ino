#include <Stepper.h>
const int stepsPerRevolution = 200, acc=30,steps=15,max_speed_UD=100,max_speed_LR=100;
int udspeed,lrspeed,X,Y;
Stepper StepperUD(stepsPerRevolution, 8, 9, 10, 11);
Stepper StepperLR(stepsPerRevolution, 2, 3, 4, 5);
void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  int xch=0,dirx=1,diry=1;
  String x="",y="";
  if(Serial.available() > 0) {
    String sensorReading = Serial.readStringUntil('\n');
    Serial.println(sensorReading);
    for(int i=0;i<=sensorReading.length();i+=1){
      if(isDigit(sensorReading[i])!= true and i!=0){
        xch=1;
      }
      if(sensorReading[i]=='-' and xch!=1 ){
        dirx=-1;
      }
      if(sensorReading[i]=='-' and xch!=0 ){
        diry=-1;
      }
      if(isDigit(sensorReading[i]) and xch!=1 ){
        x+=sensorReading[i] ;
      }
      if(isDigit(sensorReading[i]) and xch!=0){
        y+=sensorReading[i] ;
      }
    }
    X=x.toInt();
    Y=y.toInt();
    //continue here
    Serial.println(X);
    Serial.println(Y);
    udspeed = map(Y,0,240,25,max_speed_UD);
    lrspeed = map(X,0,320 ,25,max_speed_LR);
    Serial.println(udspeed);
    Serial.println(lrspeed);
    
    if (udspeed <= 30){
     diry=0;
    }
    
    if (lrspeed <= acc){
      dirx=0;
    }
    Serial.println(dirx);
    Serial.println(diry);
    StepperUD.setSpeed(udspeed);
    StepperUD.step(diry*steps);
    StepperLR.setSpeed(lrspeed);
    StepperLR.step(dirx*steps);
  }
}
