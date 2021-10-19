
// Here we use pin 10 of a teensy 4.1
const int PWM_PIN = 10;
const int DIR_PIN = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
}

int motorDirection = 0;

void loop() {
  // Write to the pin, values 0-256 (where 256 = always on)
  digitalWrite(DIR_PIN, motorDirection);
  analogWrite(PWM_PIN, 255);
  Serial.print("Running at speed ");
  Serial.println(255.0 / 256.0);
  delay(5000); // 5 second delay

  
  // Here we decrease power slightly
  analogWrite(PWM_PIN, 100);
  Serial.print("Running at speed ");
  Serial.println(100.0 / 256.0);
  delay(5000); // 5 second delay

  // Turn off the motor
  analogWrite(PWM_PIN, 0);
  Serial.print("Running at speed ");
  Serial.println(0.0 / 256.0);
  delay(2000); // 2 second delay

  // This simply flips the direction.
  motorDirection = !motorDirection;
}
