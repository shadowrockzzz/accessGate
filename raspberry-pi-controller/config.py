# config.py

# --- MQTT Broker Settings ---
MQTT_BROKER = "test.mosquitto.org" # Replace with your broker IP or domain
MQTT_PORT = 1883
MQTT_CLIENT_ID = "rpi-gate-controller"
MQTT_KEEPALIVE = 60

# --- MQTT Topics ---
TOPIC_ACCESS = "gate/access"
TOPIC_COMMAND = "gate/cmd"

# --- Hardware Settings ---
# GPIO Pin connected to the relay that controls the gate boom
RELAY_PIN = 17 

# --- Authorized RFID Tags (UIDs) ---
# Add the UIDs of your authorized RFID chips here
AUTHORIZED_TAGS = [
    123456789, 
    987654321
]