#include <Arduino.h>
#include <SPI.h>
#include "printf.h"
#include "RF24.h"

// RGB led connected to RP2040
#define LED_R 0
#define LED_G 1
#define LED_B 2

// PIR sensor connected to RP2040
#define PIR_IN 3

// Boost converter connected to RP2040
#define B_EN 9
#define B_IADJ 10

// NRF24L01+ radio connected to RP2040
#define CE_PIN 5
#define CSN_PIN 8

// Function prototypes
bool isMotionDetected();

// NRF24L01+ radio
RF24 radio(CE_PIN, CSN_PIN);
uint8_t address[][6] = { "1Node", "2Node" };

bool radioNumber = 1;
bool role = false;  // true = TX role, false = RX role

struct PayloadStruct {
  char message[7];  // only using 6 characters for TX & ACK payloads
  uint8_t counter;
};
PayloadStruct payload;

void setup() {
  Serial.begin(115200);

  while (!Serial) {
    // some boards need to wait to ensure access to serial over USB
  }
  Serial.println("IOT_2023 project startup....");

  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);

  pinMode(PIR_IN, INPUT);

  pinMode(B_EN, OUTPUT);
  pinMode(B_IADJ, OUTPUT);

  digitalWrite(LED_R, HIGH);

  // Setup 
  if (!radio.begin()) {
    Serial.println(F("radio hardware is not responding!!"));
    while (1) {}  // hold in infinite loop
  }

  radio.setPALevel(RF24_PA_LOW);  // RF24_PA_MAX is default.
  radio.enableDynamicPayloads();
  radio.enableAckPayload();
  radio.openWritingPipe(address[radioNumber]);
  radio.openReadingPipe(1, address[!radioNumber]);

  digitalWrite(LED_R, LOW);
  digitalWrite(LED_G, HIGH);

  Serial.println("IOT_2023 project startup complete");
}

void loop() {
  // put your main code here, to run repeatedly:
}

bool isMotionDetected() {
  return digitalRead(PIR_IN) == HIGH;
}
