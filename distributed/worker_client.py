import socket
import time
import logging
import uuid
import sys
from distributed.work_order import WorkOrder, GameResult
from factory.game_runner import GameRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Worker - %(levelname)s - %(message)s')
logger = logging.getLogger("worker_client")

class WorkerClient:
    def __init__(self, host='127.0.0.1', port=9871):
        self.host = host
        self.port = port
        self.worker_id = f"worker_{uuid.uuid4().hex[:8]}"
        self.runner = GameRunner(log_dir="logs")
        
    def start(self):
        logger.info(f"Worker {self.worker_id} starting...")
        while True:
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((self.host, self.port))
                
                conn.sendall(b"GET_WORK\n")
                
                data = conn.recv(8192)
                if not data:
                    conn.close()
                    continue
                    
                msg = data.decode('utf-8').strip()
                if not msg:
                    conn.close()
                    continue
                    
                order = WorkOrder.deserialize(msg)
                logger.info(f"Received work order: {order.job_id} (Iteration {order.iteration})")
                
                try:
                    res_dict = self.runner.run_iteration(
                        iteration_id=order.iteration,
                        version_n1="base", version_n2="new",
                        deck_base={}, deck_new={},
                        reasoning_base={}, reasoning_new={}
                    )
                    
                    metrics = {"completed": 1.0}
                    if "games" in res_dict and "deck_test" in res_dict["games"]:
                        win = res_dict["games"]["deck_test"].get("winner")
                        metrics["win_rate"] = 1.0 if win == "player_a" else 0.0
                
                    result = GameResult(
                        job_id=order.job_id,
                        iteration=order.iteration,
                        worker_id=self.worker_id,
                        metrics=metrics
                    )
                    
                    conn.sendall(f"RESULT:{result.serialize()}\n".encode('utf-8'))
                    
                    ack = conn.recv(1024)
                    if ack.strip() == b"ACK":
                        logger.info(f"Successfully submitted result for {order.job_id}")
                except Exception as e:
                    logger.error(f"Error running iteration: {e}")
                    
                conn.close()
                
            except ConnectionRefusedError:
                logger.warning(f"Connection refused to {self.host}:{self.port}. Master may be down.")
                raise ConnectionError("Master is down")
            except Exception as e:
                logger.error(f"Worker error: {e}")
                raise ConnectionError(f"Worker error: {e}")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    WorkerClient(host=host).start()
