/*
 * GateAccess MVP — ESP32 (Arduino framework)
 * Same MQTT contract as raspberry-pi-controller + react-native-app:
 *   publish  gate/access  -> GRANTED | DENIED | REMOTE_UNLOCK
 *   subscribe gate/cmd    -> {"action":"unlock"}
 *
 * Arduino IDE: open this folder (gate_access.ino) as a sketch.
 * Libraries: MFRC522, PubSubClient (Library Manager).
 * Board: ESP32 Dev Module (or your ESP32 board).
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include "config.h"

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
MFRC522 mfrc522(RFID_SS_PIN, RFID_RST_PIN);

unsigned long lastMqttAttemptMs = 0;
unsigned long lastTagMs = 0;

void setRelay(bool openGate) {
  bool level = RELAY_ACTIVE_HIGH ? openGate : !openGate;
  digitalWrite(RELAY_PIN, level ? HIGH : LOW);
}

void triggerGate() {
  Serial.println("Opening Gate...");
  setRelay(true);
  delay(1000);
  setRelay(false);
  Serial.println("Gate Closed.");
}

bool isAuthorized(unsigned long uid) {
  for (size_t i = 0; i < AUTHORIZED_TAG_COUNT; i++) {
    if (AUTHORIZED_TAGS[i] == uid) return true;
  }
  return false;
}

unsigned long uidToNumber(MFRC522::Uid *uid) {
  unsigned long n = 0;
  // Pack up to 4 bytes (common MIFARE Classic). Extra bytes ignored for MVP.
  byte len = uid->size < 4 ? uid->size : 4;
  for (byte i = 0; i < len; i++) {
    n = (n << 8) | uid->uidByte[i];
  }
  return n;
}

void publishAccess(const char *status) {
  if (!mqtt.connected()) return;
  mqtt.publish(TOPIC_ACCESS, status);
  Serial.print("Published ");
  Serial.print(TOPIC_ACCESS);
  Serial.print(" = ");
  Serial.println(status);
}

void handleCommand(char *topic, byte *payload, unsigned int length) {
  if (strcmp(topic, TOPIC_COMMAND) != 0) return;

  char buf[96];
  if (length >= sizeof(buf)) length = sizeof(buf) - 1;
  memcpy(buf, payload, length);
  buf[length] = '\0';

  Serial.print("MQTT cmd: ");
  Serial.println(buf);

  // MVP parse: look for "unlock" inside {"action":"unlock"}
  if (strstr(buf, "unlock") != NULL) {
    Serial.println("Remote Unlock Command Received!");
    triggerGate();
    publishAccess("REMOTE_UNLOCK");
  }
}

void connectWifi() {
  Serial.print("WiFi connecting to ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("WiFi OK, IP=");
  Serial.println(WiFi.localIP());
}

void connectMqtt() {
  if (mqtt.connected()) return;
  unsigned long now = millis();
  if (now - lastMqttAttemptMs < 3000) return;
  lastMqttAttemptMs = now;

  Serial.print("MQTT connecting ");
  Serial.println(MQTT_BROKER);
  if (mqtt.connect(MQTT_CLIENT_ID)) {
    Serial.println("MQTT connected");
    mqtt.subscribe(TOPIC_COMMAND);
  } else {
    Serial.print("MQTT failed, rc=");
    Serial.println(mqtt.state());
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("GateAccess ESP32 starting...");

  pinMode(RELAY_PIN, OUTPUT);
  setRelay(false);

  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("MFRC522 ready");

  connectWifi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(handleCommand);
  connectMqtt();

  Serial.println("Waiting for RFID tag...");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }
  if (!mqtt.connected()) {
    connectMqtt();
  }
  mqtt.loop();

  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  unsigned long now = millis();
  if (now - lastTagMs < 2000) {
    mfrc522.PICC_HaltA();
    return;
  }
  lastTagMs = now;

  unsigned long tagId = uidToNumber(&mfrc522.uid);
  Serial.print("Tag Detected: ");
  Serial.println(tagId);

  if (isAuthorized(tagId)) {
    Serial.println("Access Granted");
    publishAccess("GRANTED");
    triggerGate();
  } else {
    Serial.println("Access Denied");
    publishAccess("DENIED");
  }

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}
