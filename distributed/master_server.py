import socket
import threading
import time
import json
import logging
from queue import Queue
from collections import deque
from distributed.work_order import WorkOrder, GameResult
from factory.game_runner import GameRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Master - %(levelname)s - %(message)s')
logger = logging.getLogger("master_server")

class MasterServer:
    def __init__(self, port=9871):
        self.port = port
        self.workers = deque()
        self.work_queue = Queue()
        self.results_queue = Queue()
        self.lock = threading.Lock()
        self.running = True
        
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(10)
        logger.info(f"Master server listening on port {self.port}")
        
        threading.Thread(target=self._hybrid_runner_loop, daemon=True).start()
        threading.Thread(target=self._process_results, daemon=True).start()
        
        try:
            while self.running:
                conn, addr = self.server_socket.accept()
                logger.info(f"Worker connected from {addr}")
                threading.Thread(target=self._handle_worker, args=(conn, addr), daemon=True).start()
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            self.server_socket.close()
            
    def _handle_worker(self, conn, addr):
        with self.lock:
            self.workers.append(conn)
        try:
            while self.running:
                data = conn.recv(4096)
                if not data: break
                
                msg = data.decode('utf-8').strip()
                if msg == "GET_WORK":
                    # Wait for work if queue is empty
                    while self.work_queue.empty() and self.running:
                        time.sleep(0.5)
                    if not self.running: break
                    
                    order = self.work_queue.get()
                    conn.sendall((order.serialize() + "\n").encode('utf-8'))
                elif msg.startswith("RESULT:"):
                    result_data = msg[7:]
                    try:
                        res = GameResult.deserialize(result_data)
                        self.results_queue.put(res)
                        conn.sendall(b"ACK\n")
                    except Exception as e:
                        logger.error(f"Error parsing result from {addr}: {e}")
        except Exception as e:
            logger.info(f"Worker {addr} disconnected: {e}")
        finally:
            with self.lock:
                if conn in self.workers:
                    self.workers.remove(conn)
            conn.close()

    def _hybrid_runner_loop(self):
        # The hybrid background game runner
        runner = GameRunner(log_dir="logs")
        iteration = 1
        
        # We periodically push work into the queue
        while self.running:
            if self.work_queue.qsize() < 10:
                order = WorkOrder(job_id=f"job_{iteration}", iteration=iteration, config={"base": "aggro", "new": "control"})
                self.work_queue.put(order)
                iteration += 1
                
                # Hybrid behavior: if no workers are connected, run one locally
                with self.lock:
                    num_workers = len(self.workers)
                
                if num_workers == 0 and not self.work_queue.empty():
                    logger.info("No workers available. Running hybrid local iteration.")
                    local_order = self.work_queue.get()
                    try:
                        res_dict = runner.run_iteration(
                            iteration_id=local_order.iteration,
                            version_n1="base", version_n2="new",
                            deck_base={}, deck_new={},
                            reasoning_base={}, reasoning_new={}
                        )
                        logger.info(f"Local iteration {local_order.iteration} completed.")
                    except Exception as e:
                        logger.error(f"Local runner failed: {e}")
            time.sleep(1)

    def _process_results(self):
        while self.running:
            res = self.results_queue.get()
            logger.info(f"Collected result from {res.worker_id} for iteration {res.iteration}. Metrics: {res.metrics}")
            # Optionally write to results file or push to learner

if __name__ == "__main__":
    MasterServer().start()
