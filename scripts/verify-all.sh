#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Pi MQTT smoke (TCP 1883) =="
cd "$ROOT/raspberry-pi-controller"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements-smoke.txt
fi
.venv/bin/python mqtt_smoke_test.py

echo ""
echo "== React Native broker smoke (WS 8080) =="
cd "$ROOT/react-native-app"
if [[ ! -d node_modules ]]; then
  npm install
fi
for attempt in 1 2 3 4 5; do
  if node scripts/verify-mqtt.js; then
    break
  fi
  if [[ "$attempt" -eq 5 ]]; then
    echo "WebSocket MQTT verify failed after 5 attempts (broker may be flaky)."
    exit 1
  fi
  sleep 2
done

echo ""
echo "== Controller sim (one authorized tag) =="
cd "$ROOT/raspberry-pi-controller"
SIM_LOG="$(mktemp)"
PYTHONUNBUFFERED=1 GATE_SIM_TAG=123456789 timeout 5 .venv/bin/python -u main.py --sim >"$SIM_LOG" 2>&1 || true
grep -q "Access Granted" "$SIM_LOG" || {
  cat "$SIM_LOG"
  exit 1
}
rm -f "$SIM_LOG"
echo "OK: main.py --sim granted authorized tag"

echo ""
echo "All automated checks passed. See TESTING.md and esp32-arduino-controller/README.md."
