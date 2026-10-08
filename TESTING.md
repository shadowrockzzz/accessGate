# Initial testing checklist

## 1. MQTT (any PC — no hardware)

```bash
cd raspberry-pi-controller
python3 -m venv .venv
.venv/bin/pip install -r requirements-smoke.txt
.venv/bin/python mqtt_smoke_test.py
```

Or from repo root: `bash scripts/verify-all.sh`

Expect: three `OK:` lines and `All MQTT smoke tests passed.`

## 2. Controller logic + MQTT (PC sim — Pi path only)

Terminal A:

```bash
cd raspberry-pi-controller
.venv/bin/pip install -r requirements-smoke.txt
.venv/bin/python main.py --sim
```

Terminal B (after A shows “Waiting for RFID tag…”):

```bash
GATE_SIM_TAG=123456789 .venv/bin/python -c "
import paho.mqtt.client as c, time, config
m=c.Client(); m.connect(config.MQTT_BROKER,config.MQTT_PORT,60); m.loop_start()
time.sleep(1); m.publish('gate/cmd','{\"action\":\"unlock\"}'); time.sleep(2); m.loop_stop()
"
```

Expect on A: remote unlock and/or GRANTED/DENIED; relay `[SIM]` lines on unlock/grant.

## 3. React Native app broker (Node)

```bash
cd react-native-app
npm install
node scripts/verify-mqtt.js
```

Expect: `OK: WebSocket MQTT path (React Native broker) works.`

## 4. ESP32 (Arduino — recommended hardware test)

1. Edit `esp32-arduino-controller/gate_access/config.h` (Wi‑Fi SSID/password, pins, `AUTHORIZED_TAGS`).
2. Arduino IDE: install **ESP32** board support + libraries **MFRC522**, **PubSubClient**.
3. Open `gate_access/gate_access.ino` → Upload to ESP32 (USB).
4. Serial Monitor **115200**: `WiFi OK`, `MQTT connected`, `Waiting for RFID tag...`
5. Tap tags → note `Tag Detected:` → add UIDs to `AUTHORIZED_TAGS` → re-upload.
6. Phone app **ONLINE** → **Remote Unlock** → Serial shows remote unlock; app log `REMOTE_UNLOCK`.

Full wiring and install: [esp32-arduino-controller/README.md](esp32-arduino-controller/README.md)

## 5. Raspberry Pi (optional hardware)

```bash
sudo raspi-config   # enable SPI
cd raspberry-pi-controller
pip3 install -r requirements.txt
# Set real UIDs in config.py AUTHORIZED_TAGS
python3 main.py
```

## 6. Phone app (needs RN Android project)

`react-native-app/` is **source only**. Create RN 0.73 project, copy `App.js`, `index.js`, `src/`, merge `package.json` deps.

In `android/app/src/main/AndroidManifest.xml`: `INTERNET` + `android:usesCleartextTraffic="true"`.

Run on device; MQTT **ONLINE**; Remote Unlock should trigger controller `REMOTE_UNLOCK` (ESP32 or Pi).
