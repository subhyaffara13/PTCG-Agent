from . import LOG_COLLECTOR_PORT, Queue, QueueFull, json, logging, socket, threading, time

class TCPLogHandler(logging.Handler):
    def __init__(self, host, port=LOG_COLLECTOR_PORT, worker_id="unknown", maxsize=1000):
        super().__init__()
        self.host = host
        self.port = port
        self.worker_id = worker_id
        self._queue = Queue(maxsize=maxsize)
        self._conn = None
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._sender, daemon=True)
        self._thread.start()

    def emit(self, record):
        try:
            msg = self.format(record)
            entry = {
                "timestamp": record.created,
                "level": record.levelname,
                "name": record.name,
                "message": msg,
                "worker_id": self.worker_id
            }
            self._queue.put_nowait(entry)
        except QueueFull:
            pass

    def _sender(self):
        while True:
            try:
                entry = self._queue.get()
                self._send(entry)
            except Exception:
                time.sleep(0.5)

    def _send(self, entry):
        with self._lock:
            if self._conn is None:
                try:
                    self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._conn.settimeout(5.0)
                    self._conn.connect((self.host, self.port))
                except Exception:
                    self._conn = None
                    time.sleep(1)
                    return
            try:
                self._conn.sendall((json.dumps(entry) + "\n").encode("utf-8"))
            except Exception:
                try:
                    self._conn.close()
                except Exception:
                    pass
                self._conn = None

