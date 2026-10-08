#!/usr/bin/env python3
"""Generate beginner GateAccess setup PDF."""
from pathlib import Path

from fpdf import FPDF, XPos, YPos

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "image.jpeg"
OUT = ROOT / "GateAccess_Beginner_Guide.pdf"


class GuidePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.set_x(10)
        self.cell(190, 8, "GateAccess MVP - Beginner Setup Guide")
        self.ln(4)
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def ensure_space(self, h=30):
        if self.get_y() > 297 - 18 - h:
            self.add_page()

    def h1(self, text):
        self.ensure_space(40)
        self.set_x(10)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(20, 40, 80)
        self.multi_cell(190, 9, text)
        self.ln(2)

    def h2(self, text):
        self.ensure_space(28)
        self.ln(2)
        self.set_x(10)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 70, 120)
        self.multi_cell(190, 7, text)
        self.ln(1)

    def h3(self, text):
        self.ensure_space(22)
        self.ln(1)
        self.set_x(10)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(190, 6, text)
        self.ln(0.5)

    def body(self, text):
        self.set_x(10)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(190, 5.4, text)
        self.ln(1.2)

    def bullet(self, text):
        self.set_x(10)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(6, 5.4, "-")
        self.multi_cell(184, 5.4, text)
        self.ln(0.4)

    def numbered(self, n, text):
        self.set_x(10)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(8, 5.4, f"{n}.")
        self.multi_cell(182, 5.4, text)
        self.ln(0.6)

    def note(self, text):
        self.ensure_space(25)
        self.set_x(10)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(30, 70, 120)
        self.multi_cell(190, 5, "IMPORTANT")
        self.set_x(10)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(190, 5, text)
        self.ln(2)

    def code(self, text):
        self.ensure_space(20)
        self.set_font("Courier", "", 8)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(20, 20, 20)
        for line in text.strip("\n").split("\n"):
            self.set_x(10)
            self.cell(190, 4.6, "  " + line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(2)

    def kv(self, key, value):
        self.ensure_space(16)
        self.set_x(10)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(20, 20, 20)
        self.cell(50, 6, key, border=1)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(140, 6, value, border=1)


def build():
    pdf = GuidePDF(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(10, 12, 10)
    pdf.add_page()

    # Cover
    pdf.set_y(25)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 40, 80)
    pdf.set_x(10)
    pdf.multi_cell(190, 12, "GateAccess MVP", align="C")
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_x(10)
    pdf.multi_cell(190, 9, "Complete Beginner Setup Guide", align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.set_x(10)
    pdf.multi_cell(
        190,
        6,
        "How to add an ESP32 (Arduino) or Raspberry Pi to your gate box,\n"
        "upload/run the controller, connect MQTT, and control the gate\n"
        "from the React Native phone app.",
        align="C",
    )
    pdf.ln(6)
    if IMAGE.exists():
        pdf.image(str(IMAGE), x=25, w=160)
        pdf.ln(3)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_x(10)
        pdf.multi_cell(190, 5, "Your control enclosure (image.jpeg)", align="C")

    # 1
    pdf.add_page()
    pdf.h1("1. What this project does (simple words)")
    pdf.body(
        "You have a control box that opens a gate boom barrier. Today that box already has "
        "power, wiring, and an old computer board (the blue board in the photo). "
        "We will add a new small controller board as the brain. For MVP we recommend "
        "ESP32 (Arduino, low cost). Raspberry Pi is optional for future camera work. "
        "The controller will:"
    )
    pdf.bullet("Read RFID chips (tags) with an RFID scanner.")
    pdf.bullet("If the chip is allowed, open the gate for about 1 second using a relay.")
    pdf.bullet("Talk to your phone app over the internet using MQTT messages.")
    pdf.bullet("Also open the gate when you press Remote Unlock in the app.")
    pdf.body(
        "MVP means Minimum Viable Product: make it work first. The UI does not need to look fancy."
    )
    pdf.note(
        "You are NOT flashing firmware into the blue/green boards in the photo. "
        "You ADD an ESP32 or Raspberry Pi, upload/run our scripts on THAT board, and rewire "
        "RFID + gate open signal to it. Backup the blue board first."
    )

    pdf.h2("1.1 Parts of the system")
    pdf.kv("Control box", "Enclosure in your photo - power, boards, terminals")
    pdf.kv("ESP32 (Arduino)", "Recommended MVP - Wi-Fi, ~300-800 INR board")
    pdf.kv("Raspberry Pi", "Optional - Python, better for future camera")
    pdf.kv("RFID reader", "Module that reads chip UIDs over SPI")
    pdf.kv("RFID chips/tags", "Cards/keyfobs people tap to enter")
    pdf.kv("Relay", "Electronic switch that pulses the boom open")
    pdf.kv("MQTT broker", "Public message post office: test.mosquitto.org")
    pdf.kv("Phone app", "React Native app installed on your Android phone")

    # 2
    pdf.h1("2. Looking at your box (image.jpeg)")
    pdf.body("Match these labels to what you see inside the open enclosure:")

    pdf.h3("Top - Power Supply Unit (PSU)")
    pdf.body(
        "Large metal unit with a honeycomb/mesh cover. Thick wires leave its terminals. "
        "This powers the whole system. Keep it. The ESP32/Pi will take 5V from here "
        "(USB adapter, or buck converter from 12V/24V if you know how to wire safely)."
    )

    pdf.h3("Center - Blue board with gold heatsink")
    pdf.body(
        "This is the CURRENT brain (old single-board computer). You may see USB ports, "
        "a power jack, Ethernet, and a ribbon cable. Do NOT delete its software yet. "
        "First back it up. Later the ESP32 or Pi replaces its job for our MVP."
    )

    pdf.h3("Right - Green board")
    pdf.body(
        "Secondary / interface board. Often has network (Ethernet cable plugged in). "
        "Usually leave it alone unless RFID or relay is wired only through it."
    )

    pdf.h3("Middle - Gray terminal blocks (DIN rail)")
    pdf.body(
        "Long row of screw terminals. Field cables (boom open signal, sensors, ground) "
        "land here. This is the MOST IMPORTANT area for wiring: connect the new controller "
        "so it drives the same open-gate path the old board used."
    )

    pdf.h3("Bottom - Cable glands")
    pdf.body(
        "Thick cables leave the box to the boom and possibly an external RFID reader. "
        "A good area to mount the ESP32 or Pi (not under the hot PSU)."
    )

    # 3
    pdf.add_page()
    pdf.h1("3. How MQTT works here (for beginners)")
    pdf.body(
        "MQTT is a simple messaging system. Think of a post office (the broker). "
        "The controller (ESP32 or Pi) and the phone do not call each other directly. "
        "Both connect to the same broker and leave/pick up messages on named topics (mailboxes)."
    )

    pdf.h3("Broker we use for MVP testing")
    pdf.body("Host: test.mosquitto.org (public test broker - fine for learning, not for production secrets).")
    pdf.bullet("ESP32 / Raspberry Pi connect with TCP on port 1883")
    pdf.bullet("Phone app connects with WebSocket: ws://test.mosquitto.org:8080")
    pdf.body("Both still share the SAME topics, so they can talk through that broker.")

    pdf.h3("Topics (the mailboxes)")
    pdf.kv("gate/cmd", "Phone publishes unlock. Example: {\"action\":\"unlock\"}")
    pdf.kv("gate/access", "Controller publishes GRANTED, DENIED, or REMOTE_UNLOCK")

    pdf.h3("Flow A - Someone taps an authorized RFID chip")
    pdf.code(
        "RFID chip -> RFID reader (SPI) -> ESP32 or Pi controller\n"
        "  -> checks AUTHORIZED_TAGS (config.h or config.py)\n"
        "  -> turns relay ON for 1 second (boom opens)\n"
        "  -> publishes gate/access = GRANTED\n"
        "  -> phone app log shows GRANTED"
    )

    pdf.h3("Flow B - You press Remote Unlock in the phone app")
    pdf.code(
        "Phone app -> publishes gate/cmd {\"action\":\"unlock\"}\n"
        "  -> broker delivers message to controller\n"
        "  -> controller turns relay ON for 1 second\n"
        "  -> publishes gate/access = REMOTE_UNLOCK\n"
        "  -> phone log shows REMOTE_UNLOCK"
    )

    pdf.note(
        "The boom itself is NOT opened over MQTT. MQTT only carries messages. "
        "Opening the gate is always local wiring: GPIO -> relay -> terminals -> boom."
    )

    pdf.h3("Where is the app hosted?")
    pdf.body(
        "For this MVP the React Native app is NOT a website on a server. "
        "You install it on an Android phone. It only needs internet so it can reach "
        "the MQTT broker. The ESP32 or Pi is the controller in/near the box. "
        "Later you can distribute the APK via Play Store or an internal link - that is "
        "app distribution, not gate-control hosting."
    )

    # 4
    pdf.add_page()
    pdf.h1("4. What to do BEFORE you touch wires")
    pdf.numbered(1, "Take clear photos of every cable and terminal label (door legend too).")
    pdf.numbered(2, "Label wires with tape if labels are missing.")
    pdf.numbered(3, "Backup old scripts from the blue board (USB copy / SSH / disk image).")
    pdf.numbered(4, "Power OFF the enclosure before changing wiring.")
    pdf.numbered(5, "Confirm boom open voltage/safety with someone who knows the site if unsure.")
    pdf.numbered(
        6,
        "Have ready: ESP32 dev board (recommended) OR Raspberry Pi kit, 5V power, "
        "RFID module, relay module (if not already present), Wi-Fi with internet.",
    )
    pdf.note(
        "If you are unsure which terminal opens the boom, do NOT guess with live power. "
        "Trace from the old board relay output to the terminals while powered down."
    )

    # 5
    pdf.h1("5. Where to inject the controller (ESP32 or Pi)")
    pdf.h2("5.1 Physical placement")
    pdf.bullet("Mount the board in free space (often near the bottom cable area).")
    pdf.bullet("Use standoffs so it does not short against metal.")
    pdf.bullet("Keep it away from the hot PSU at the top.")
    pdf.bullet("Route cables neatly; leave slack for future service.")

    pdf.h2("5.2 Power inject")
    pdf.bullet("ESP32: often 5V via USB phone charger or regulated 5V/GND.")
    pdf.bullet("Pi: stable 5V with enough current; buck converter from 12V/24V if needed.")
    pdf.bullet("Share common ground (GND) between controller, relay module, and existing logic.")

    pdf.h2("5.3 Network inject")
    pdf.bullet("ESP32: Wi-Fi only - set SSID/password in config.h; needs internet for MQTT.")
    pdf.bullet("Pi: Ethernet or Wi-Fi; test: ping test.mosquitto.org")

    pdf.h2("5.4 RFID inject (MFRC522 SPI)")
    pdf.bullet("Document then disconnect RFID SPI from the old blue board.")
    pdf.bullet("Wire RFID to the new board (3.3V logic only).")
    pdf.bullet("ESP32 default pins: SS=5, RST=22, SCK/MOSI/MISO as in esp32 README.")
    pdf.bullet("Pi: enable SPI via raspi-config.")

    pdf.h2("5.5 Gate / boom inject (most important)")
    pdf.body(
        "Find how the OLD system opens the boom (relay input or dry contact into terminals). "
        "Move that CONTROL INPUT to the new controller:"
    )
    pdf.code(
        "ESP32 GPIO 26 (default) --> Relay IN\n"
        "Pi GPIO BCM 17 (default) --> Relay IN\n"
        "Relay COM/NO --> same boom-open terminals the old board used"
    )
    pdf.body(
        "ESP32: edit RELAY_PIN in gate_access/config.h. Pi: edit RELAY_PIN in config.py."
    )

    pdf.h2("5.6 ESP32 wiring quick table (defaults in our sketch)")
    pdf.kv("MFRC522 SDA", "ESP32 GPIO 5")
    pdf.kv("MFRC522 RST", "ESP32 GPIO 22")
    pdf.kv("Relay IN", "ESP32 GPIO 26")
    pdf.kv("MFRC522 power", "3.3V and GND (not 5V on ESP32 GPIO)")

    # 6
    pdf.add_page()
    pdf.h1("6. Software: scripts from start (step by step)")
    pdf.h2("6.1 Files you care about")
    pdf.kv("gate_access.ino", "ESP32 main sketch (recommended)")
    pdf.kv("config.h (ESP32)", "Wi-Fi, MQTT, pins, AUTHORIZED_TAGS")
    pdf.kv("main.py", "Pi program (optional)")
    pdf.kv("config.py (Pi)", "Broker, topics, GPIO, tags")
    pdf.kv("react-native-app/", "Phone app (App.js + mqttService.js)")
    pdf.kv("TESTING.md / README.md", "Checklists and quick links")

    pdf.h2("6.2 Desk test first (no enclosure needed)")
    pdf.body("On your laptop, from the GateAccess folder:")
    pdf.code(
        "bash scripts/verify-all.sh\n"
        "\n"
        "# Optional: simulate controller without GPIO/RFID\n"
        "cd raspberry-pi-controller\n"
        "python3 -m venv .venv\n"
        ".venv/bin/pip install -r requirements-smoke.txt\n"
        ".venv/bin/python main.py --sim"
    )
    pdf.body(
        "In --sim mode you can type a tag UID. Sample authorized IDs in config.py are "
        "123456789 and 987654321 - replace these with real chip IDs later."
    )

    pdf.h2("6.3 ESP32 (Arduino IDE) - recommended")
    pdf.numbered(1, "Install Arduino IDE + ESP32 board support (Espressif).")
    pdf.numbered(2, "Library Manager: install MFRC522 and PubSubClient.")
    pdf.numbered(3, "Open esp32-arduino-controller/gate_access/gate_access.ino")
    pdf.numbered(4, "Edit config.h: WIFI_SSID, WIFI_PASSWORD, pins if needed.")
    pdf.numbered(5, "Connect ESP32 by USB, select ESP32 Dev Module, click Upload.")
    pdf.numbered(6, "Serial Monitor 115200: WiFi OK, MQTT connected, Waiting for RFID tag...")
    pdf.body(
        "Tap each chip; copy Tag Detected numbers into AUTHORIZED_TAGS in config.h; upload again."
    )

    pdf.h2("6.4 Raspberry Pi (optional)")
    pdf.numbered(1, "Flash Raspberry Pi OS, enable SPI, copy raspberry-pi-controller/ to Pi.")
    pdf.numbered(2, "pip install -r requirements.txt; edit config.py; run python3 main.py.")

    pdf.h2("6.5 Learn RFID chip numbers")
    pdf.body(
        "ESP32: Serial Monitor line Tag Detected. Pi: console Tag Detected. "
        "Use the number from the controller you actually run (they may differ slightly)."
    )

    pdf.h2("6.6 Phone app (React Native)")
    pdf.body(
        "The react-native-app folder is APP SOURCE. Create a React Native Android project "
        "shell once, then copy our files in:"
    )
    pdf.code(
        "npx @react-native-community/cli@latest init GateAccessApp --version 0.73.0\n"
        "# Copy into that project: App.js, index.js, src/\n"
        "# Merge package.json dependencies from our package.json\n"
        "# In android/app/src/main/AndroidManifest.xml add:\n"
        "#   INTERNET permission\n"
        "#   android:usesCleartextTraffic=\"true\" on <application>\n"
        "npm install\n"
        "npm run android"
    )
    pdf.body(
        "When the app opens: MQTT should become ONLINE. Press Remote Unlock. "
        "Controller should show remote unlock and the relay should click / boom pulse."
    )

    # 7
    pdf.add_page()
    pdf.h1("7. Full inject day checklist (on the real machine)")
    pdf.numbered(1, "Power OFF enclosure. Photograph wiring.")
    pdf.numbered(2, "Mount ESP32 (or Pi) + 5V power + Wi-Fi/network.")
    pdf.numbered(3, "Wire RFID SPI to the new controller.")
    pdf.numbered(4, "Wire relay IN to GPIO (ESP32: 26 default, Pi: 17 default).")
    pdf.numbered(5, "Upload sketch (ESP32) or run main.py (Pi).")
    pdf.numbered(6, "Capture tag UIDs into config.h or config.py; re-upload/restart.")
    pdf.numbered(7, "Tap authorized tag: boom opens about 1s; app shows GRANTED.")
    pdf.numbered(8, "Press Remote Unlock on phone: boom opens; app shows REMOTE_UNLOCK.")
    pdf.numbered(9, "Tap unauthorized tag: DENIED; boom stays closed.")
    pdf.numbered(10, "Only after this works, decide whether to retire old blue-board software.")

    pdf.h1("8. Common problems")
    pdf.kv("ESP32 WiFi fails", "SSID/password in config.h; 2.4 GHz Wi-Fi; signal in box")
    pdf.kv("ESP32 MQTT fails", "Internet on Wi-Fi; broker test.mosquitto.org:1883")
    pdf.kv("Pi cannot connect MQTT", "Internet? ping test.mosquitto.org")
    pdf.kv("App stays OFFLINE", "Phone internet; cleartext traffic; WS port 8080")
    pdf.kv("No RFID reads", "SPI enabled? 3.3V? Wiring MOSI/MISO/SCK/SS/RST?")
    pdf.kv("Tag always DENIED", "UID missing from AUTHORIZED_TAGS (exact number)")
    pdf.kv("MQTT works, boom silent", "Relay wiring / wrong terminal / GPIO pin mismatch")
    pdf.kv("Relay chatters or sticks", "Power/GND issues; relay may need separate supply")
    pdf.kv("Public broker slow/flaky", "Retry; later use your own Mosquitto server")

    pdf.h1("9. Safety notes")
    pdf.bullet("Gate barriers can injure people - keep the area clear while testing.")
    pdf.bullet("Isolate mains voltage; as a beginner, work only on low-voltage control signals.")
    pdf.bullet("test.mosquitto.org is public. For real sites use a private broker with authentication.")
    pdf.bullet("Do not leave the enclosure open outdoors; reseal glands and door.")

    pdf.h1("10. Quick reference")
    pdf.code(
        "Controller: test.mosquitto.org:1883 (ESP32 + Pi)\n"
        "App:        ws://test.mosquitto.org:8080\n"
        "Topics:     gate/cmd  |  gate/access\n"
        "ESP32:      gate_access.ino + config.h, relay GPIO 26\n"
        "Pi:         main.py + config.py, relay GPIO 17\n"
        "Verify:     bash scripts/verify-all.sh"
    )

    pdf.ln(3)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 40, 80)
    pdf.multi_cell(190, 7, "Next action")
    pdf.set_x(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(
        190,
        5.4,
        "1) Run Section 6.2 desk verify. 2) Upload ESP32 sketch (Section 6.3). "
        "3) Follow Section 7 on the real box. See esp32-arduino-controller/README.md "
        "for wiring details.",
    )

    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
