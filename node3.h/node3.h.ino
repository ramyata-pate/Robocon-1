#include <ros.h>
#include <std_msgs/Float64MultiArray.h>
int pwmFL=2;
int pwmRL=3;
int pwmFR=4;
int pwmRR=5;

int FL1=22;
int FL2=23;
int RL1=24;
int RL2=25;
int FR1=27;
int FR2=26;
int RR1=28;
int RR2=29;

ros::NodeHandle nh;

int callback(std_msgs::Float64& vel[])
{
  digitalWrite(FL1,HIGH);
  digitalWrite(FL2,LOW);
  digitalWrite(FR1,HIGH);
  digitalWrite(FR2,LOW);
  digitalWrite(RR1,HIGH);
  digitalWrite(RR2,LOW);
  digitalWrite(RL1,HIGH);
  digitalWrite(RL2,LOW);
  analogWrite(pwmFL,vel[0]);
  analogWrite(pwmFR,vel[1]);
  analogWrite(pwmRL,vel[2]);
  analogWrite(pwmRR,vel[3]);
  return 1;
}

ros::Subscriber<std_msgs::Float64> sub("vel_topic", &callback);

void setup() 
{
  nh.initNode();
  nh.subscribe(sub);
  pinMode(pwmFL,OUTPUT);
  pinMode(pwmRL,OUTPUT);
  pinMode(pwmFR,OUTPUT);
  pinMode(pwmRR,OUTPUT);
  pinMode(FL1,OUTPUT);
  pinMode(FL2,OUTPUT);
  pinMode(RL1,OUTPUT);
  pinMode(RL2,OUTPUT);
  pinMode(FR1,OUTPUT);
  pinMode(FR2,OUTPUT);
  pinMode(RR1,OUTPUT);
  pinMode(RR2,OUTPUT); 
}

void loop() 
{
  nh.spinOnce();

}
