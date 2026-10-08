# ESP32 gate controller (Arduino)

**Recommended MVP controller** (low cost in India, ~₹300–800 for the board). Uses the **same MQTT topics** as `react-native-app` and `raspberry-pi-controller`.

See also: [../TESTING.md](../TESTING.md), [../GateAccess_Beginner_Guide.pdf](../GateAccess_Beginner_Guide.pdf), [../README.md](../README.md).

| Topic | Direction | Payload |
|-------|-----------|---------|
| `gate/access` | ESP32 → phone | `GRANTED` / `DENIED` / `REMOTE_UNLOCK` |
| `gate/cmd` | phone → ESP32 | `{"action":"unlock"}` |

## Hardware

- **ESP32** dev board (Wi‑Fi)
- **MFRC522** RFID (SPI)
- **Relay module** → same boom-open path as in your enclosure

### Default wiring (ESP32 ↔ MFRC522)

| MFRC522 | ESP32 |
|---------|-------|
| SDA (SS) | GPIO 5 |
| SCK | GPIO 18 |
| MOSI | GPIO 23 |
| MISO | GPIO 19 |
| RST | GPIO 22 |
| 3.3V | 3.3V |
| GND | GND |

Relay **IN** → GPIO **26** (change `RELAY_PIN` in `config.h` if needed).

## Software setup (Arduino IDE)

1. Install [Arduino IDE](https://www.arduino.cc/en/software).
2. **Board manager:** add ESP32 by Espressif (Boards Manager → search “esp32”).
3. Select board **ESP32 Dev Module**.
4. **Libraries** (Library Manager):
   - `MFRC522` by GithubCommunity
   - `PubSubClient` by Nick O'Leary
5. Open sketch folder: `esp32-arduino-controller/gate_access/gate_access.ino`
6. Edit `config.h`: Wi‑Fi SSID/password, `AUTHORIZED_TAGS`, pins if needed.
7. Plug ESP32 via USB → **Upload**.
8. **Tools → Serial Monitor** @ **115200** → tap RFID tags to read UIDs.

## On-site install (your metal box)

1. **Backup** the blue board software; power **off**.
2. Mount ESP32 inside/near the box (do **not** flash the blue board).
3. Move **RFID SPI** and **relay control** wires to the ESP32 (same roles as for Pi).
4. Power ESP32 (USB adapter or 5V/GND from a safe tap — not mains without experience).
5. ESP32 must reach **Wi‑Fi with internet** (for `test.mosquitto.org`).
6. Upload sketch once from laptop; then it runs standalone after reset.

## Test with phone app

1. ESP32 running, Serial shows `MQTT connected`.
2. Open React Native app → **ONLINE**.
3. **Remote Unlock** → Serial: remote unlock, relay click, app log `REMOTE_UNLOCK`.
4. Authorized tag → `GRANTED` + 1s relay pulse.

## Notes

- UID numbers on ESP32 may differ from Pi encoding; always use the number printed on **ESP32 Serial Monitor**.
- Public broker is for MVP only; use a private broker for production.
- If relay never clicks, try `RELAY_ACTIVE_HIGH = false` in `config.h`.
