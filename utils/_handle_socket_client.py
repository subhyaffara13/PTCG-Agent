import json

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

