import socket, threading, json
from . import logger

def _socket_listener_loop(self):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(128)
        server_socket.settimeout(1.0)
    except Exception as e:
        logger.error(f"InferenceServer socket bind failed on port {self.port}: {e}")
        return
    while self._running:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(target=self._handle_socket_client, args=(conn,), daemon=True).start()
        except socket.timeout:
            continue
        except Exception:
            break
    server_socket.close()

def _handle_socket_client(self, conn):
    try:
        rfile = conn.makefile('r', encoding='utf-8')
        wfile = conn.makefile('w', encoding='utf-8')
        for line in rfile:
            if not self._running: break
            line = line.strip()
            if not line: continue
            state_data = json.loads(line)
            logits, value = self.predict(state_data)
            wfile.write(json.dumps({"logits": logits, "value": value}) + "\n")
            wfile.flush()
    except Exception:
        pass
    finally:
        try: conn.close()
        except Exception: pass
