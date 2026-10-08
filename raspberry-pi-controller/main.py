# main.py
import argparse
import os
import time
import json
import paho.mqtt.client as mqtt
import config

parser = argparse.ArgumentParser(description="Gate controller (use --sim on PC without GPIO/RFID)")
parser.add_argument("--sim", action="store_true", help="Simulate relay and RFID (MQTT still real)")
args = parser.parse_args()

if args.sim:

    class _SimGPIO:
        BCM = OUT = None
        HIGH = 1
        LOW = 0

        @staticmethod
        def setwarnings(_):
            pass

        @staticmethod
        def setmode(_):
            pass

        @staticmethod
        def setup(*_a, **_k):
            pass

        @staticmethod
        def output(pin, value):
            print(f"[SIM] Relay pin {pin} -> {'OPEN' if value else 'CLOSED'}")

        @staticmethod
        def cleanup():
            pass

    GPIO = _SimGPIO

    class _SimReader:
        def read(self):
            preset = os.environ.get("GATE_SIM_TAG")
            if preset:
                return int(preset), ""
            print("[SIM] Type RFID UID and Enter (empty = 123456789): ", end="", flush=True)
            line = input().strip()
            return (int(line) if line else 123456789), ""

    reader = _SimReader()
else:
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.RELAY_PIN, GPIO.OUT)
    GPIO.output(config.RELAY_PIN, GPIO.LOW)
    reader = SimpleMFRC522()

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # Subscribe to the command topic when connected
    client.subscribe(config.TOPIC_COMMAND)

def on_message(client, userdata, msg):
    """Handles incoming remote commands from the React Native App."""
    if msg.topic == config.TOPIC_COMMAND:
        try:
            payload = json.loads(msg.payload.decode())
            if payload.get("action") == "unlock":
                print("Remote Unlock Command Received!")
                trigger_gate()
                client.publish(config.TOPIC_ACCESS, "REMOTE_UNLOCK")
        except json.JSONDecodeError:
            print("Invalid JSON received")

def trigger_gate():
    """Activates the relay to open the gate boom for 1 second."""
    print("Opening Gate...")
    GPIO.output(config.RELAY_PIN, GPIO.HIGH)
    time.sleep(1) # Keep gate open for 1 second
    GPIO.output(config.RELAY_PIN, GPIO.LOW)
    print("Gate Closed.")

# --- Main Application ---
def main():
    # Setup MQTT Client
    client = mqtt.Client(client_id=config.MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"Connecting to MQTT Broker at {config.MQTT_BROKER}...")
    client.connect(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_KEEPALIVE)
    client.loop_start() # Start MQTT loop in a separate thread

    try:
        while True:
            print("Waiting for RFID tag...")
            # Read RFID tag (This blocks until a tag is read)
            tag_id, text = reader.read()
            print(f"Tag Detected: {tag_id}")

            if tag_id in config.AUTHORIZED_TAGS:
                print("Access Granted")
                client.publish(config.TOPIC_ACCESS, "GRANTED")
                trigger_gate()
            else:
                print("Access Denied")
                client.publish(config.TOPIC_ACCESS, "DENIED")
            
            time.sleep(2) # Prevents reading the same tag multiple times instantly

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()