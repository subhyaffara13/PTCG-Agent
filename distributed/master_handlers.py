import time
import logging
from distributed.work_order import GameResult

logger = logging.getLogger("master_server")

class MasterHandlers:
    def __init__(self, server):
        self.server = server

    def handle_worker(self, conn, addr):
        with self.server.lock:
            self.server.workers.append(conn)
        try:
            while self.server.running:
                try:
                    data = conn.recv(4096)
                    if not data: break
                except Exception as e:
                    logger.info(f"Worker recv error {addr}: {e}")
                    break
                
                msg = data.decode('utf-8').strip()
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
        while self.server.running:
            res = self.server.results_queue.get()
            logger.info(f"Collected result from {res.worker_id} for iteration {res.iteration}.")
