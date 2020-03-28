#include <Servo.h>
#include<MsTimer2.h>
#include<Arduino.h>
#include "HX711.h"
#include <LiquidCrystal_I2C.h>
#include<ros.h>
#include<geometry_msgs/Twist.h>
ros::NodeHandle nh;

/*load cell HX711*/
const int DT_PIN = 34;
const int SCK_PIN = 36;
HX711 Scale;
int gram = 0;
int prevGram = 0;
/*LCD I2C*/
LiquidCrystal_I2C lcd(0x27,16,2);
/*servo motor*/
Servo lid_opener;
int pinLid = 5;
int lid_angle = 0;
/*servo motor angle*/
const int open_angle = 130;
const int close_angle = 0;
/*timer*/
int count_time = 0;
volatile boolean tim1msF = false;
/*right motor pin*/
const int pinR1 = 6;
const int pinR2 = 7;
/*left motor pin*/
const int pinL1 = 12;
const int pinL2 = 11;
/*pwm value*/
const int pwmR = 200;
const int pwmL = 200;
/*finish flag*/
int flagR = false;
int flagL = false;
/*pwmR ecoder pin*/
const int encR1 = 3;
const int encR2 = 2;
/*pwmL encoder pin*/
const int encL1 = 18;
const int encL2 = 19;
//encoder value
volatile double pulseR = 0, pulseL = 0;
volatile uint8_t prevR = 0, prevL = 0;
/*encoder calculation variable*/
double radian;
double target_pulse;
double target_pulse_minus;
double motor_degree;
int absolute_distance;
int absolute_angle;
const double wheel_radius = 2.2;
/*ppr : pulse per revolution*/
const int ppr = 133;
/*ppd : pulse per degree*/
double ppd;

/*[駆動モータ(右)のエンコーダ]*/
void updateEncoderR(){
  uint8_t a = digitalRead(encR1);
  uint8_t b = digitalRead(encR2);
  uint8_t ab = (a << 1) | b;
  uint8_t encR  = (prevR << 2) | ab;
  if(encR == 0b1101 || encR == 0b0100 || encR == 0b0010 || encR == 0b1011){
    pulseR ++;
  }else if(encR == 0b1110 || encR == 0b0111 || encR == 0b0001 || encR == 0b1000) {
    pulseR --;
  }
  prevR = ab;
}

/*[駆動モータ(左)のエンコーダ]*/
void updateEncoderL(){
  uint8_t c = digitalRead(encL1);
  uint8_t d = digitalRead(encL2);
  uint8_t cd = (c << 1) | d;
  uint8_t encL  = (prevL << 2) | cd;
  if(encL == 0b1101 || encL == 0b0100 || encL == 0b0010 || encL == 0b1011){
    pulseL ++;
  }else if(encL == 0b1110 || encL == 0b0111 || encL == 0b0001 || encL == 0b1000) {
    pulseL --;
  }
  prevL = cd;
}

/*[タイマー割込み(nミリ秒)]*/
void timer1mS(){
  tim1msF = true;
}
int Timer(int n){
  MsTimer2::set(1, timer1mS);
  MsTimer2::start();
  while(count_time <= n){
    if(tim1msF){
      count_time = count_time + 1;
      tim1msF = false;
    }
  }
  MsTimer2::stop();
  tim1msF = false;
  count_time = 0;
  return 0;
}

void Open(){
  for(lid_angle = close_angle; lid_angle <= open_angle; lid_angle ++){
        lid_opener.write(lid_angle);
        Timer(20);
  }
}

void Close(){
  for(lid_angle = open_angle; lid_angle >= close_angle; lid_angle --){
        lid_opener.write(lid_angle);
        Timer(20);
  }
}

void LoadCell() {
  while(1){
    nh.spinOnce();
    gram = Scale.get_units(10) + 0.5;
    lcd.init(); 
    lcd.backlight();
    lcd.setCursor(0,0);
    lcd.print("TrashBot");
    lcd.setCursor(1,2);
    lcd.print("weight: ");
    lcd.setCursor(9,2);
    lcd.print(gram);
    lcd.setCursor(15,2);
    lcd.print("(g)");
    Scale.power_down();
    Scale.power_up();
    Timer(5);
    if(gram > prevGram){
      Close();
      prevGram = gram + 1;
      break;
    }
  }
} 

/*[前方移動]*/
void Go_straight(int distance){
    if(distance > 35){
      distance = distance - 30;
    }
    absolute_distance = distance;
    radian = absolute_distance / wheel_radius;
    motor_degree = radian / PI * 180;
    /*ppd : pulse per degree*/
    ppd = 360 / ppr;
    target_pulse = motor_degree / ppd;
    
    while(distance >= 0){     
      nh.spinOnce();
      /*right motor forward*/
      if(pulseR >= target_pulse -5) {
        analogWrite(pinR1,0);
        analogWrite(pinR2,0);
        flagR = true;
      }else if (pulseR >= target_pulse -50) {
        analogWrite(pinR1,pwmR -10);
        analogWrite(pinR2,0);
      }else{
        analogWrite(pinR1,pwmR);
        analogWrite(pinR2,0);
      }
      /*left motor forward*/
      if(pulseL >= target_pulse -5){
        analogWrite(pinL1,0);
        analogWrite(pinL2,0);  
        flagL = true;  
      }else if (pulseL >= target_pulse -50) {
        analogWrite(pinL1,pwmL -10);
        analogWrite(pinL2,0);
      }else {
        analogWrite(pinL1,pwmL);
        analogWrite(pinL2,0);
      }
      /*finish conditions*/
      if(flagR == true && flagL == true){
       initialize();
       break;
      }
    }
}

/*[後方移動]*/
void Go_back(int distance){
   absolute_distance = distance*(-1);
   radian = absolute_distance / wheel_radius;
   motor_degree = radian / PI * 180;
   //ppd : pulse per degree
   ppd = 360 / ppr;
   target_pulse = (motor_degree / ppd);
   target_pulse_minus = target_pulse*(-1);
   
   while(distance < 0){
     nh.spinOnce();
     /*right motor reverse*/
     if (pulseR <= target_pulse_minus +5){
     analogWrite(pinR1,0);
     analogWrite(pinR2,0);
     flagR = true;
     }else if (pulseR <= target_pulse_minus +50){
      analogWrite(pinR1,0);
      analogWrite(pinR2,pwmR -10);
     }else{
      analogWrite(pinR1,0);
      analogWrite(pinR2,pwmR);
     }
     /*left motor reverse*/
     if(pulseL <= target_pulse_minus +5){
     analogWrite(pinL1,0);
     analogWrite(pinL2,0);
     flagL = true;
     }else if(pulseL <= target_pulse_minus +50){
      analogWrite(pinL1,0);
      analogWrite(pinL2,pwmL -10);
     }else{
      analogWrite(pinL1,0);
      analogWrite(pinL2,pwmL);
     }
     /*finish conditions*/
     if(flagR == true && flagL == true){
      initialize();
      break;
     }
   }
}

 /*[右旋回]*/
 void Turn_right(int yaw_angle){
    absolute_angle = yaw_angle;
    /*linear function of turning*/
    motor_degree = 4.3 * absolute_angle - 8.0;
    /*ppd : pulse per degree*/
    ppd = 360 / ppr;
    target_pulse = motor_degree / ppd;
    target_pulse_minus = target_pulse*(-1);
    
    while(yaw_angle >= 0){
      nh.spinOnce();
      /*right motor reverse*/
      if (pulseR <= target_pulse_minus +5){
        analogWrite(pinR1,0);
        analogWrite(pinR2,0);
        flagR = true;
      }else if (pulseR <= target_pulse_minus +50){
        analogWrite(pinR1,0);
        analogWrite(pinR2,pwmR);
      }else{
        analogWrite(pinR1,0);
        analogWrite(pinR2,pwmR +50);
      }
      /*left motor forward*/
      if(pulseL >= target_pulse -5){
        analogWrite(pinL1,0);
        analogWrite(pinL2,0);  
        flagL = true;  
      }else if(pulseL >= target_pulse -50){
        analogWrite(pinL1,pwmL);
        analogWrite(pinL2,0);
      }else{
        analogWrite(pinL1,pwmL +50);
        analogWrite(pinL2,0);
      }
      /*finish conditions*/
      if(flagR == true && flagL == true){
        initialize();
        break;
      }
    }
 }

 /*[左旋回]*/
 void Turn_left(int yaw_angle){
    absolute_angle = yaw_angle*(-1);
    /*linear function of turning*/
    motor_degree = 4.3 * absolute_angle - 8.0;
    //ppd : pulse per degree
    ppd = 360 / ppr;
    target_pulse = motor_degree / ppd;
    target_pulse_minus = target_pulse*(-1);
    
    while(yaw_angle < 0){                       
      nh.spinOnce();
      /*right motor forward*/
      if(pulseR >= target_pulse -5){
        analogWrite(pinR1,0);
        analogWrite(pinR2,0);
        flagR = true;
      }else if(pulseR >= target_pulse -50){
        analogWrite(pinR1,pwmR);
        analogWrite(pinR2,0);
      }else{
        analogWrite(pinR1,pwmR +50);
        analogWrite(pinR2,0);
      }
      /*left motor reverse*/
      if(pulseL <= target_pulse_minus +5){
        analogWrite(pinL1,0);
        analogWrite(pinL2,0);
        flagL = true;
      }else if(pulseL <= target_pulse_minus +50){
        analogWrite(pinL1,0);
        analogWrite(pinL2,pwmL);
      }else{
        analogWrite(pinL1,0);
        analogWrite(pinL2,pwmL +50);
      }
      /*finish conditions*/
      if(flagR == true && flagL == true){
        initialize();
        break;
      }
    }
 }

void initialize(){
   analogWrite(pinR1,0);
   analogWrite(pinR2,0);
   analogWrite(pinL1,0);
   analogWrite(pinL2,0);  
   flagR = false;
   flagL = false;
   pulseR = 0;
   pulseL = 0;
   target_pulse = 0;
   nh.spinOnce();
   Timer(500);
}

void Approach(int distance, int yaw_angle){
  
  if(yaw_angle >= 0) {
    Turn_right(yaw_angle);
  }  
  else if(yaw_angle < 0){
    Turn_left(yaw_angle);
  }
  
  if(distance >= 0){
    Go_straight(distance);
  }
  else if(distance < 0){
    Go_back(distance);
  }
}

void Route_order(const geometry_msgs::Twist &message){
  int CentiMeter = message.linear.x;
  int Degree = message.angular.z;
  Approach(CentiMeter, Degree);
  Timer(1000);
  Open();
  Timer(100);
  LoadCell();
  Timer(500);
  CentiMeter = -CentiMeter;
  Go_back(CentiMeter);
  Timer(2000);
}

ros::Subscriber<geometry_msgs::Twist> route_of_robot("/trashbot_command", &Route_order);
//ros::Subscriber<std_msgs::Int16> trashbot("/trashbot_command",&order);
void setup(){
  Scale.begin(DT_PIN, SCK_PIN);
  /*パラメータ設定*/
  Scale.set_scale(386.3);
  Scale.tare();
  lcd.init(); 
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("TrashBot");
  lid_opener.attach(pinLid);
  lid_opener.write(close_angle);
  pinMode(pinR1, OUTPUT);
  pinMode(pinR2, OUTPUT);
  pinMode(pinL1, OUTPUT);
  pinMode(pinL2, OUTPUT);
  pinMode(encR1, INPUT);
  pinMode(encR2, INPUT);
  pinMode(encL1, INPUT);
  pinMode(encL2, INPUT);
  digitalWrite(encR1, HIGH);
  digitalWrite(encR2, HIGH);
  digitalWrite(encL1, HIGH);
  digitalWrite(encL2, HIGH);
  attachInterrupt(0, updateEncoderR, CHANGE);
  attachInterrupt(1, updateEncoderR, CHANGE);
  attachInterrupt(5, updateEncoderL, CHANGE);
  attachInterrupt(4, updateEncoderL, CHANGE);
  nh.initNode();
  nh.subscribe(route_of_robot);
}
void loop(){
  nh.spinOnce();
  Timer(1);
}
