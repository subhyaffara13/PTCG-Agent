import socket
import time
import threading
import json
import logging

PORT = 9870
BEACON_INTERVAL = 2

class MasterBeacon:
    def __init__(self, code_version):
        self.code_version = code_version
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.running = True
        threading.Thread(target=self._broadcast_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _broadcast_loop(self):
        while self.running:
            try:
                message = json.dumps({'type': 'beacon', 'code_version': self.code_version})
                self.sock.sendto(message.encode(), ('<broadcast>', PORT))
                time.sleep(BEACON_INTERVAL)
            except Exception as e:
                logging.error(f"Beacon error: {e}")
                time.sleep(BEACON_INTERVAL)

class WorkerListener:
    def __init__(self, interface_type="ethernet"):
        self.timeout = 30 if interface_type.lower() == "wifi" else 15
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', PORT))
        self.sock.settimeout(self.timeout)

    def listen_for_master(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            msg = json.loads(data.decode())
            if msg.get('type') == 'beacon':
                return addr[0], msg.get('code_version')
        except socket.timeout:
            return None, None
        except Exception as e:
            logging.error(f"Listener error: {e}")
        return None, None
