/**
 * Same broker/topics as mqttService.js — run: node scripts/verify-mqtt.js
 */
const mqtt = require('mqtt');

const BROKER = 'ws://test.mosquitto.org:8080';
const TIMEOUT_MS = 20000;

function connect(url, clientId) {
  return new Promise((resolve, reject) => {
    const client = mqtt.connect(url, {clientId, reconnectPeriod: 0});
    const timer = setTimeout(() => {
      client.end(true);
      reject(new Error('connect timeout'));
    }, TIMEOUT_MS);
    client.on('connect', () => {
      clearTimeout(timer);
      resolve(client);
    });
    client.on('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

async function main() {
  const suffix = Date.now();
  const controller = await connect(BROKER, `rn-smoke-ctrl-${suffix}`);

  controller.on('message', (topic, payload) => {
    if (topic !== 'gate/cmd') return;
    const data = JSON.parse(payload.toString());
    if (data.action === 'unlock') {
      controller.publish('gate/access', 'REMOTE_UNLOCK');
    }
  });

  await new Promise((resolve, reject) => {
    controller.subscribe('gate/cmd', (err) => (err ? reject(err) : resolve()));
  });

  const app = await connect(BROKER, `rn-smoke-app-${suffix}`);

  const gotRemote = new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error('no REMOTE_UNLOCK')), TIMEOUT_MS);
    app.on('message', (_topic, payload) => {
      if (payload.toString() === 'REMOTE_UNLOCK') {
        clearTimeout(t);
        resolve();
      }
    });
  });

  await new Promise((resolve, reject) => {
    app.subscribe('gate/access', (err) => (err ? reject(err) : resolve()));
  });

  app.publish('gate/cmd', JSON.stringify({action: 'unlock'}));
  await gotRemote;

  app.end(true);
  controller.end(true);
  console.log('OK: WebSocket MQTT path (React Native broker) works.');
}

main().catch((e) => {
  console.error('FAIL:', e.message);
  process.exit(1);
});
