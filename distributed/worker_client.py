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
        consec_failures = 0
        while True:
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.settimeout(120.0)  # Safe timeout for MCTS runs
                conn.connect((self.host, self.port))
                consec_failures = 0  # Reset on successful connection
                
                rfile = conn.makefile('r', encoding='utf-8')
                while True:
                    conn.sendall(b"GET_WORK\n")
                    
                    data_line = rfile.readline()
                    if not data_line:
                        break
                        
                    msg = data_line.strip()
                    if not msg:
                        break
                        
                    order = WorkOrder.deserialize(msg)
                    logger.info(f"Received work order: {order.job_id} (Iteration {order.iteration})")
                    
                    try:
                        d_base = {"cards": order.deck_base} if order.deck_base else {}
                        d_new = {"cards": order.deck_new} if order.deck_new else {}
                        res_dict = self.runner.run_iteration(
                            iteration_id=order.iteration,
                            version_n1="base", version_n2="new",
                            deck_base=d_base, deck_new=d_new,
                            reasoning_base={}, reasoning_new={}
                        )
                        
                        metrics = {"completed": 1.0}
                        if "games" in res_dict and "deck_test" in res_dict["games"]:
                            win = res_dict["games"]["deck_test"].get("winner")
                            metrics["win_rate"] = 1.0 if win == "player_a" else 0.0
                    
                        from distributed.telemetry_sync import compress_telemetry
                        telemetry_data = compress_telemetry(res_dict)
                    
                        # Exclude steps_dump to keep payload size reasonable
                        games_data = res_dict.get("games", {})
                        disk_results = {label: {k: v for k, v in res.items() if k != "steps_dump"} for label, res in games_data.items()}
                        disk_payload = {
                            "iteration": order.iteration,
                            "timestamp": res_dict.get("timestamp"),
                            "games": disk_results,
                            "ready_for_eval": True
                        }

                        result = GameResult(
                            job_id=order.job_id,
                            iteration=order.iteration,
                            worker_id=self.worker_id,
                            metrics=metrics,
                            payload=disk_payload
                        )
                        result.set_replay(telemetry_data)
                        
                        conn.sendall(f"RESULT:{result.serialize()}\n".encode('utf-8'))
                        
                        ack_line = rfile.readline()
                        if not ack_line or ack_line.strip() != "ACK":
                            logger.error("Failed to receive ACK from master")
                            break
                        logger.info(f"Successfully submitted result for {order.job_id}")
                    except Exception as e:
                        logger.error(f"Error running iteration: {e}")
                        break
                        
                conn.close()
                
            except (ConnectionRefusedError, socket.error) as e:
                consec_failures += 1
                logger.warning(f"Connection error to {self.host}:{self.port} (attempt {consec_failures}): {e}. Retrying...")
                if consec_failures >= 15:
                    logger.error("Too many connection failures. Falling back to Master discovery.")
                    raise ConnectionError("Master host unreachable")
                time.sleep(10)
            except Exception as e:
                consec_failures += 1
                logger.error(f"Unexpected worker error (attempt {consec_failures}): {e}. Retrying...")
                if consec_failures >= 15:
                    logger.error("Too many connection failures. Falling back to Master discovery.")
                    raise ConnectionError("Master host unreachable")
                time.sleep(10)

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    WorkerClient(host=host).start()
