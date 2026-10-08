#pragma once

// --- Wi-Fi (edit these) ---
static const char *WIFI_SSID = "YOUR_WIFI_SSID";
static const char *WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// --- MQTT (same broker/topics as Pi + React Native app) ---
static const char *MQTT_BROKER = "test.mosquitto.org";
static const uint16_t MQTT_PORT = 1883;
static const char *MQTT_CLIENT_ID = "esp32-gate-controller";
static const char *TOPIC_ACCESS = "gate/access";
static const char *TOPIC_COMMAND = "gate/cmd";

// --- Pins (ESP32 DevKit defaults — change if your wiring differs) ---
// MFRC522 SPI: SCK=18, MISO=19, MOSI=23 on most ESP32 boards
static const uint8_t RFID_SS_PIN = 5;   // SDA / SS
static const uint8_t RFID_RST_PIN = 22; // RST
static const uint8_t RELAY_PIN = 26;    // drives relay IN (boom open)

// Relay: HIGH = open gate. Set false if your module is active-LOW.
static const bool RELAY_ACTIVE_HIGH = true;

// --- Authorized RFID UIDs (decimal, same idea as Pi config.py) ---
// Tap a card once with Serial Monitor open to see "Tag Detected: ...", then add it here.
static const unsigned long AUTHORIZED_TAGS[] = {
    123456789UL,
    987654321UL,
};
static const size_t AUTHORIZED_TAG_COUNT =
    sizeof(AUTHORIZED_TAGS) / sizeof(AUTHORIZED_TAGS[0]);
