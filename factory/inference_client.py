"""
factory/inference_client.py

Client wrapper for MCTS workers to connect to the InferenceServer via TCP sockets.
Converts game states to JSON and routes predictions over the network.
"""
import logging
import socket
import json
import threading
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class InferenceClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self.host = host
        self.port = port
        self._conn = None
        self._rfile = None
        self._wfile = None
        self._lock = threading.Lock()

    def _connect(self) -> bool:
        if self._conn is not None:
            return True
        try:
            self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._conn.settimeout(2.0)  # 2 seconds timeout
            self._conn.connect((self.host, self.port))
            self._rfile = self._conn.makefile('r', encoding='utf-8')
            self._wfile = self._conn.makefile('w', encoding='utf-8')
            return True
        except Exception:
            self._conn = None
            return False

    def evaluate(self, game_state: dict) -> Tuple[Optional[list], float]:
        """Send a game state to the inference server and get (logits, value)."""
        with self._lock:
            if not self._connect():
                return None, 0.0
            try:
                # Strip out objects to keep JSON small
                filtered_state = {k: v for k, v in game_state.items() if not k.startswith("_")}
                payload = json.dumps(filtered_state) + "\n"
                self._wfile.write(payload)
                self._wfile.flush()
                
                response_line = self._rfile.readline()
                if not response_line:
                    self.close()
                    return None, 0.0
                res = json.loads(response_line)
                return res.get("logits"), res.get("value", 0.0)
            except Exception:
                self.close()
                return None, 0.0

    def is_available(self) -> bool:
        """Check if the inference server is running and connectable."""
        with self._lock:
            return self._connect()

    def close(self):
        try:
            if self._conn:
                self._conn.close()
        except Exception:
            pass
        self._conn = None
        self._rfile = None
        self._wfile = None
