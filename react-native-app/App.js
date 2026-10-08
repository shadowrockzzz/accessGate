import React, {useEffect, useState} from 'react';
import {
  SafeAreaView,
  View,
  Text,
  Pressable,
  ScrollView,
  StyleSheet,
  StatusBar,
} from 'react-native';
import mqttService from './src/mqttService';

export default function App() {
  const [connected, setConnected] = useState(false);
  const [lastStatus, setLastStatus] = useState('—');
  const [logs, setLogs] = useState([]);

  const addLog = (line) => {
    const ts = new Date().toLocaleTimeString();
    setLogs((prev) => [`[${ts}] ${line}`, ...prev].slice(0, 50));
  };

  useEffect(() => {
    mqttService.connect(
      (topic, message) => {
        setLastStatus(message);
        addLog(`${topic}: ${message}`);
      },
      (ok) => {
        setConnected(ok);
        addLog(ok ? 'Connected to broker' : 'Disconnected');
      },
    );
    return () => mqttService.disconnect();
  }, []);

  const onUnlock = () => {
    if (mqttService.unlock()) {
      addLog('Sent unlock command');
    } else {
      addLog('Not connected — unlock failed');
    }
  };

  const statusColor =
    lastStatus === 'GRANTED' || lastStatus === 'REMOTE_UNLOCK'
      ? '#2e7d32'
      : lastStatus === 'DENIED'
        ? '#c62828'
        : '#555';

  return (
    <SafeAreaView style={styles.root}>
      <StatusBar barStyle="dark-content" />
      <Text style={styles.title}>Gate Access</Text>

      <View style={styles.row}>
        <Text style={styles.label}>MQTT</Text>
        <Text style={{color: connected ? '#2e7d32' : '#c62828', fontWeight: '700'}}>
          {connected ? 'ONLINE' : 'OFFLINE'}
        </Text>
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Last event</Text>
        <Text style={{color: statusColor, fontWeight: '700'}}>{lastStatus}</Text>
      </View>

      <Pressable
        style={[styles.btn, !connected && styles.btnDisabled]}
        onPress={onUnlock}
        disabled={!connected}>
        <Text style={styles.btnText}>Remote Unlock</Text>
      </Pressable>

      <Text style={styles.logTitle}>Log</Text>
      <ScrollView style={styles.logBox}>
        {logs.map((l, i) => (
          <Text key={i} style={styles.logLine}>
            {l}
          </Text>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  root: {flex: 1, backgroundColor: '#f5f5f5', padding: 16},
  title: {fontSize: 22, fontWeight: '700', marginBottom: 16},
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  label: {fontSize: 16, color: '#333'},
  btn: {
    marginTop: 24,
    backgroundColor: '#1565c0',
    paddingVertical: 14,
    alignItems: 'center',
  },
  btnDisabled: {backgroundColor: '#90a4ae'},
  btnText: {color: '#fff', fontSize: 16, fontWeight: '700'},
  logTitle: {marginTop: 24, marginBottom: 8, fontWeight: '700'},
  logBox: {flex: 1, backgroundColor: '#fff', padding: 8, borderWidth: 1, borderColor: '#ddd'},
  logLine: {fontSize: 12, fontFamily: 'monospace', marginBottom: 4, color: '#222'},
});
