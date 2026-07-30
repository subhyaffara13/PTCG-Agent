from . import LOG_COLLECTOR_PORT, json, logging, os, socket, threading, time

class LogCollectorServer:
    def __init__(self, log_dir="logs/worker_logs", port=LOG_COLLECTOR_PORT):
        self.port = port
        self.log_dir = log_dir
        self.running = True
        os.makedirs(log_dir, exist_ok=True)
        self._logger = logging.getLogger("log_collector")

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True, name="log-collector")
        thread.start()
        return thread

    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('0.0.0.0', self.port))
            sock.listen(10)
            sock.settimeout(1.0)
            self._logger.info(f"Log collector listening on port {self.port}")
        except Exception as e:
            self._logger.error(f"Failed to bind log collector on port {self.port}: {e}")
            return

        while self.running:
            try:
                conn, addr = sock.accept()
                self._logger.info(f"Log connection from {addr}")
                t = threading.Thread(target=self._handle, args=(conn, addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self._logger.error(f"Log collector accept error: {e}")

        sock.close()

    def _handle(self, conn, addr):
        worker_id = None
        rfile = conn.makefile('r', encoding='utf-8')
        try:
            while self.running:
                line = rfile.readline()
                if not line:
                    break
                try:
                    record = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                wid = record.get("worker_id", "unknown")
                if worker_id is None:
                    worker_id = wid
                    fpath = os.path.join(self.log_dir, f"{worker_id}.log")
                    f = open(fpath, "a", encoding="utf-8")
                    self._logger.info(f"Logging {worker_id} to {fpath}")

                ts = record.get("timestamp", time.time())
                level = record.get("level", "INFO")
                name = record.get("name", "")
                msg = record.get("message", "")
                f.write(f"{ts} - {name} - {level} - {msg}\n")
                f.flush()
        except Exception:
            pass
        finally:
            if worker_id:
                try:
                    f.close()
                except Exception:
                    pass
            conn.close()

