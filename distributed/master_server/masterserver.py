from . import GameResult, GameRunner, MasterHandlers, Queue, WorkOrder, deque, get_local_version, logger, socket, threading, time
from ._load_deck import _load_deck

class MasterServer:
    def __init__(self, port=9871):
        self.port = port
        self.workers = deque()
        self.work_queue = Queue()
        self.results_queue = Queue()
        self.lock = threading.Lock()
        self.running = True
        self.handlers = MasterHandlers(self)
        
    def _accept_with_timeout(self, timeout: float = 1.0):
        """Accept a connection with a timeout so shutdown doesn't block forever."""
        self.server_socket.settimeout(timeout)
        try:
            return self.server_socket.accept()
        except socket.timeout:
            return None, None
        finally:
            self.server_socket.settimeout(None)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(10)
        logger.info(f"Master server listening on port {self.port}")
        
        threading.Thread(target=self._hybrid_runner_loop, daemon=True).start()
        threading.Thread(target=self.handlers.process_results, daemon=True).start()
        # Start UDP beacon so workers can auto-discover the master
        try:
            from distributed.discovery import MasterBeacon
            self.beacon = MasterBeacon(code_version=get_local_version())
            self.beacon.start()
        except Exception as e:
            logger.warning(f"Failed to start master beacon: {e}")
        
        # Start process_results background thread to collect worker results and trigger PPO trainer
        threading.Thread(target=self.handlers.process_results, daemon=True).start()

        try:
            while self.running:
                conn, addr = self._accept_with_timeout(1.0)
                if conn is None:
                    continue
                logger.info(f"Worker connected from {addr}")
                threading.Thread(target=self.handlers.handle_worker, args=(conn, addr), daemon=True).start()
        except Exception as e:
            if self.running:
                logger.error(f"Server error: {e}")
        finally:
            self.server_socket.close()

    def stop(self):
        self.running = False
        try:
            self.server_socket.close()
        except:
            pass

    def _hybrid_runner_loop(self):
        runner = GameRunner(log_dir="logs")
        iteration = 1
        startup_time = time.time()
        grace_period = 120  # 2 minutes grace period to search for workers
        
        while self.running:
            if self.work_queue.qsize() < 10:
                d_base = _load_deck("cb_agents/deck_base.csv")
                d_new = _load_deck("cb_agents/deck_new.csv")
                
                from distributed.code_sync import get_local_version
                master_version = get_local_version()
                
                order = WorkOrder(
                    job_id=f"job_{iteration}",
                    iteration=iteration,
                    config={"base": "aggro", "new": "control"},
                    deck_base=d_base,
                    deck_new=d_new,
                    code_version=master_version
                )
                self.work_queue.put(order)
                iteration += 1
                
            with self.lock:
                num_workers = len(self.workers)
            
            if num_workers == 0 and not self.work_queue.empty():
                elapsed = time.time() - startup_time
                if elapsed < grace_period:
                    remaining = int(grace_period - elapsed)
                    logger.info(f"No workers connected yet. Waiting for workers to join (grace period: {remaining}s remaining)...")
                    time.sleep(5)
                else:
                    logger.info("No workers connected and grace period expired. Running hybrid local iteration.")
                    local_order = self.work_queue.get()
                    t0 = time.time()
                    try:
                        # Reduce game count from 61 to 13 (num_matchups=3) when running without workers
                        # MCTS runs within 5s actTimeout; concede logic aborts hopeless games early
                        res_dict = runner.run_iteration(
                            iteration_id=local_order.iteration,
                            version_n1="base", version_n2="new",
                            deck_base={"cards": local_order.deck_base},
                            deck_new={"cards": local_order.deck_new},
                            reasoning_base={}, reasoning_new={},
                            num_matchups=3
                        )
                        elapsed_iter = time.time() - t0
                        logger.info(f"Local iteration {local_order.iteration} completed in {elapsed_iter:.1f}s.")
                        
                        from distributed.work_order import GameResult
                        metrics = {"completed": 1.0}
                        if "games" in res_dict and "deck_test" in res_dict["games"]:
                            win = res_dict["games"]["deck_test"].get("winner")
                            metrics["win_rate"] = 1.0 if win == "player_a" else 0.0

                        games_data = res_dict.get("games", {})
                        disk_results = {label: {k: v for k, v in res.items() if k != "steps_dump"} for label, res in games_data.items()}
                        disk_payload = {
                            "iteration": local_order.iteration,
                            "timestamp": res_dict.get("timestamp"),
                            "games": disk_results,
                            "ready_for_eval": True
                        }

                        result = GameResult(
                            job_id=local_order.job_id,
                            iteration=local_order.iteration,
                            worker_id="local_fallback",
                            metrics=metrics,
                            payload=disk_payload
                        )
                        self.results_queue.put(result)
                        logger.info(f"Submitted local fallback GameResult to results_queue for iteration {local_order.iteration}")
                    except Exception as e:
                        logger.error(f"Local runner failed: {e}")
            else:
                time.sleep(1)

