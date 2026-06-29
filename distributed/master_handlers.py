import time
import logging
from distributed.work_order import GameResult

logger = logging.getLogger("master_server")

def _read_line(conn):
    buf = bytearray()
    while True:
        try:
            chunk = conn.recv(65536)
            if not chunk:
                return None
            buf.extend(chunk)
            if b'\n' in chunk:
                break
        except Exception:
            return None
    return buf.decode('utf-8')

class MasterHandlers:
    def __init__(self, server):
        self.server = server

    def handle_worker(self, conn, addr):
        with self.server.lock:
            self.server.workers.append(conn)
        try:
            while self.server.running:
                msg_line = _read_line(conn)
                if not msg_line: break
                msg = msg_line.strip()
                if msg == "GET_WORK":
                    while self.server.work_queue.empty() and self.server.running:
                        time.sleep(0.5)
                    if not self.server.running: break
                    
                    order = self.server.work_queue.get()
                    try:
                        conn.sendall((order.serialize() + "\n").encode('utf-8'))
                    except Exception as e:
                        logger.error(f"Error sending work to {addr}: {e}")
                        # Put work back on queue
                        self.server.work_queue.put(order)
                        break
                elif msg.startswith("RESULT:"):
                    result_data = msg[7:]
                    try:
                        res = GameResult.deserialize(result_data)
                        self.server.results_queue.put(res)
                        conn.sendall(b"ACK\n")
                    except Exception as e:
                        logger.error(f"Error parsing result from {addr}: {e}")
                        break
        except Exception as e:
            logger.info(f"Worker {addr} disconnected: {e}")
        finally:
            with self.server.lock:
                if conn in self.server.workers:
                    self.server.workers.remove(conn)
            conn.close()

    def process_results(self):
        from distributed.telemetry_sync import decompress_telemetry
        while self.server.running:
            res = self.server.results_queue.get()
            logger.info(f"Collected result from {res.worker_id} for iteration {res.iteration}.")
            try:
                telemetry_data = res.get_replay()
                if telemetry_data:
                    decompress_telemetry(telemetry_data)
            except Exception as e:
                logger.error(f"Error extracting telemetry from {res.worker_id}: {e}")
