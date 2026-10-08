import mqtt from 'mqtt';

// Public Mosquitto WebSocket (works in RN without native TCP modules)
const BROKER_URL = 'ws://test.mosquitto.org:8080';
const CLIENT_ID = 'rn-gate-app-' + Math.random().toString(16).slice(2, 8);

class MqttService {
  constructor() {
    this.client = null;
    this.isConnected = false;
  }

  connect(onMessage, onStatus) {
    if (this.client) this.disconnect();

    this.client = mqtt.connect(BROKER_URL, {
      clientId: CLIENT_ID,
      clean: true,
      reconnectPeriod: 3000,
    });

    this.client.on('connect', () => {
      this.isConnected = true;
      onStatus(true);
      this.client.subscribe('gate/access');
    });

    this.client.on('message', (topic, payload) => {
      onMessage(topic, payload.toString());
    });

    this.client.on('close', () => {
      this.isConnected = false;
      onStatus(false);
    });

    this.client.on('error', (err) => {
      console.error('MQTT error:', err.message);
      onStatus(false);
    });
  }

  unlock() {
    if (!this.client || !this.isConnected) return false;
    this.client.publish('gate/cmd', JSON.stringify({action: 'unlock'}));
    return true;
  }

  disconnect() {
    if (this.client) {
      this.client.end(true);
      this.client = null;
      this.isConnected = false;
    }
  }
}

export default new MqttService();
