#include <Servo.h>
const int max_bound_forx=120,min_bound_forx=50,max_bound_fory=120,min_bound_fory=50,steps=2,accX=15,accY=15;
int posud=90,poslr=90,X,Y;
Servo Sud, Slr; 
void setup() {
  Serial.begin(9600);
  Sud.attach(10);
  Slr.attach(9);
}

void loop() {
  int xch=0,dirX=1,dirY=1;
  String x="",y="";
  if(Serial.available() > 0) {
    String sensorReading = Serial.readStringUntil('\n');
    Serial.println(sensorReading);
    for(int i=0;i<=sensorReading.length();i+=1){
      if(isDigit(sensorReading[i])!= true and i!=0){
        xch=1;
      }
      if(sensorReading[i]=='-' and xch!=1 ){
        dirX=-1;
      }
      if(sensorReading[i]=='-' and xch!=0 ){
        dirY=-1;
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
    X=X*dirX;
    Y=Y*dirY;
    X = map(X,0,640,-320,320);
    Y = map(Y,0,480,-240,240);
    Serial.println(X);
    Serial.println(Y);
    if (X>=accX and poslr<=max_bound_forx){
      poslr=poslr + steps;
    }
    if (X<=-accX and poslr>=min_bound_forx){
      poslr=poslr - steps;
    }
    if (Y>=accY and posud <=max_bound_fory){
      posud=posud + steps;
    }
    if (Y<=-accY and posud>=min_bound_fory){
      posud=posud - steps;
    }
    Sud.write(posud);
    Slr.write(poslr);
  }
}
