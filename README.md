# GateAccess MVP

RFID gate boom control with **MQTT** and a **React Native** phone app.

## Choose a controller (pick one)

| Controller | Folder | Cost (India, rough) | Best for |
|------------|--------|---------------------|----------|
| **ESP32 (Arduino)** | `esp32-arduino-controller/` | ~₹300–800 board | **MVP / budget** — Wi‑Fi built-in |
| **Raspberry Pi** | `raspberry-pi-controller/` | ~₹15k+ kit | Future **camera**, more CPU |

You add a **separate board** inside/near the metal box. You do **not** flash the existing blue board in the enclosure.

## MQTT (same for ESP32, Pi, and app)

| Topic | Direction | Payload |
|-------|-----------|---------|
| `gate/access` | Controller → phone | `GRANTED` / `DENIED` / `REMOTE_UNLOCK` |
| `gate/cmd` | phone → controller | `{"action":"unlock"}` |

- **Controller:** `test.mosquitto.org:1883` (TCP)
- **Phone app:** `ws://test.mosquitto.org:8080` (WebSocket)

## Repo layout

```
GateAccess/
  esp32-arduino-controller/   ← ESP32 sketch + README (recommended start)
  raspberry-pi-controller/      ← Python on Pi (optional)
  react-native-app/             ← Phone app source
  TESTING.md                    ← Test checklist
  GateAccess_Beginner_Guide.pdf ← Full beginner guide (regenerate below)
  image.jpeg                    ← Your enclosure photo
  scripts/verify-all.sh         ← MQTT smoke tests (no hardware)
```

## Quick start

**ESP32:** see [esp32-arduino-controller/README.md](esp32-arduino-controller/README.md)

**Desk MQTT test (no hardware):**

```bash
bash scripts/verify-all.sh
```

**Regenerate PDF guide:**

```bash
.pdf-venv/bin/python scripts/make_beginner_guide_pdf.py
```

(First time: `python3 -m venv .pdf-venv && .pdf-venv/bin/pip install fpdf2`)
