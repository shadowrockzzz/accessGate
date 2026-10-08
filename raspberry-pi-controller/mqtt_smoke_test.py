#!/usr/bin/env python3
"""End-to-end MQTT check (no Pi hardware). Run: python3 mqtt_smoke_test.py"""
import json
import sys
import threading
import time
import uuid

import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_ACCESS = "gate/access"
TOPIC_CMD = "gate/cmd"
TIMEOUT = 20


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"OK: {msg}")


def main():
    suffix = uuid.uuid4().hex[:8]
    got_unlock_cmd = threading.Event()
    got_remote_unlock = threading.Event()
    got_granted = threading.Event()
    controller_ready = threading.Event()

    def on_controller_connect(client, userdata, flags, rc):
        if rc != 0:
            fail(f"controller connect rc={rc}")
        client.subscribe(TOPIC_CMD, qos=0)
        controller_ready.set()

    def on_controller_message(client, userdata, msg):
        if msg.topic != TOPIC_CMD:
            return
        payload = json.loads(msg.payload.decode())
        if payload.get("action") == "unlock":
            got_unlock_cmd.set()
            client.publish(TOPIC_ACCESS, "REMOTE_UNLOCK")

    controller = mqtt.Client(client_id=f"gate-smoke-ctrl-{suffix}")
    controller.on_connect = on_controller_connect
    controller.on_message = on_controller_message
    controller.connect(BROKER, PORT, 60)
    controller.loop_start()

    if not controller_ready.wait(TIMEOUT):
        fail("controller did not connect/subscribe in time")

    app = mqtt.Client(client_id=f"gate-smoke-app-{suffix}")

    def on_app_connect(client, userdata, flags, rc):
        if rc != 0:
            fail(f"app connect rc={rc}")
        client.subscribe(TOPIC_ACCESS, qos=0)

    def on_app_message(client, userdata, msg):
        body = msg.payload.decode()
        if body == "REMOTE_UNLOCK":
            got_remote_unlock.set()
        if body == "GRANTED":
            got_granted.set()

    app.on_connect = on_app_connect
    app.on_message = on_app_message
    app.connect(BROKER, PORT, 60)
    app.loop_start()
    time.sleep(2)

    app.publish(TOPIC_CMD, json.dumps({"action": "unlock"}), qos=0)
    if not got_unlock_cmd.wait(TIMEOUT):
        fail("controller did not receive unlock on gate/cmd")
    ok("gate/cmd unlock received")

    if not got_remote_unlock.wait(TIMEOUT):
        fail("app did not receive REMOTE_UNLOCK on gate/access")
    ok("gate/access REMOTE_UNLOCK received")

    controller.publish(TOPIC_ACCESS, "GRANTED", qos=0)
    if not got_granted.wait(TIMEOUT):
        fail("app did not receive GRANTED on gate/access")
    ok("gate/access GRANTED received")

    app.loop_stop()
    controller.loop_stop()
    app.disconnect()
    controller.disconnect()
    print("\nAll MQTT smoke tests passed.")


if __name__ == "__main__":
    main()
