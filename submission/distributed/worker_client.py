import sys
import os
import subprocess
import time
import io

# Ensure root directory is in python path for clean package imports
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

# First ensure_dependencies definition removed

import contextlib

class DummyStream(io.StringIO):
    def write(self, s):
        return len(s)
    def flush(self):
        pass

@contextlib.contextmanager
def silence_kaggle_warnings():
    import builtins
    import sys
    orig_print = builtins.print
    def dummy_print(*args, **kwargs):
        if args and isinstance(args[0], str) and ("Loading environment" in args[0] and "failed" in args[0]):
            return
        orig_print(*args, **kwargs)
    builtins.print = dummy_print
    
    # Hide pyspiel module from python loader during import to bypass OpenSpiel C++ prints
    saved_pyspiel = sys.modules.get('pyspiel')
    sys.modules['pyspiel'] = None  # type: ignore
    
    dummy_stream = DummyStream()
    try:
        with contextlib.redirect_stderr(dummy_stream), contextlib.redirect_stdout(dummy_stream):
            yield
    finally:
        builtins.print = orig_print
        if saved_pyspiel is not None:
            sys.modules['pyspiel'] = saved_pyspiel
        else:
            sys.modules.pop('pyspiel', None)

def ensure_dependencies():
    # Purge any old colliding test_agents compiled bytecode cache files in root folder
    try:
        import pathlib
        root_dir = pathlib.Path(__file__).parent.parent.resolve()
        for p in root_dir.glob("__pycache__/test_agents*"):
            if p.is_file():
                p.unlink()
        for p in root_dir.glob("test_agents*"):
            if p.is_file() and p.suffix in (".pyc", ".pyo"):
                p.unlink()
    except Exception:
        pass

    required_packages = ["numpy", "pydantic", "pokerkit", "dotenv", "kaggle_environments"]
    missing = False
    for pkg in required_packages:
        try:
            if pkg == "dotenv":
                import dotenv
            else:
                with silence_kaggle_warnings():
                    __import__(pkg)
        except ImportError:
            missing = True
            break
            
    if missing:
        print("Missing dependencies detected. Satisfying requirements...")
        try:
            # 1. Install kaggle-environments with --no-deps to completely bypass pygame build errors!
            print("Installing kaggle-environments without dependencies (avoids compiling pygame)...")
            subprocess.run([sys.executable, "-m", "pip", "install", "kaggle-environments", "--no-deps"], check=True)
            
            # 2. Locate and install other dependencies via requirements.txt
            req_path = os.path.join(os.getcwd(), "requirements.txt")
            if os.path.exists(req_path):
                print("Installing requirements.txt...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "install", "numpy", "pandas", "torch", "redis", "pydantic", "pokerkit", "python-dotenv", "requests", "jsonschema", "flask", "urllib3"], check=True)
            print("Dependencies successfully installed!")
        except Exception as e:
            print(f"Failed to auto-install dependencies: {e}.")
            
        # Verify if everything was resolved
        still_missing = []
        for pkg in required_packages:
            try:
                if pkg == "dotenv":
                    import dotenv
                else:
                    with silence_kaggle_warnings():
                        __import__(pkg)
            except ImportError:
                still_missing.append(pkg)
                
        if still_missing:
            print("\n" + "="*80)
            print(f"CRITICAL ERROR: The following packages are still missing: {still_missing}")
            print("Please run manually on this machine:")
            print("  pip install " + " ".join(still_missing))
            print("="*80 + "\n")
            print("Worker will pause for 60 seconds before exiting to prevent infinite crash loops...")
            time.sleep(60)
            sys.exit(1)

import socket
import logging
import uuid
from distributed.work_order import WorkOrder, GameResult
from factory.game_runner import GameRunner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Worker - %(levelname)s - %(message)s')
logger = logging.getLogger("worker_client")

_MAX_RETRIES = 15
_CONNECT_TIMEOUT = 5.0  # Short timeout for initial TCP connect
_READ_TIMEOUT = 120.0    # Longer timeout for MCTS runs (per-read)
_STARTUP_WATCHDOG = 300  # 5 minutes: if we can't get a complete cycle, bail

def _backoff_sleep(attempt: int):
    """Exponential backoff: 1, 2, 4, 8, 16, 30, 30, ... seconds."""
    delay = min(30, 2 ** attempt)
    time.sleep(delay)

class WorkerClient:
    def __init__(self, host='127.0.0.1', port=9871):
        self.host = host
        self.port = port
        self.worker_id = f"worker_{uuid.uuid4().hex[:8]}"
        self.runner = GameRunner(log_dir="logs")
        self.last_git_check = time.time()
        self.shutdown_requested = False
        self._startup_time = time.time()
        
        from distributed.code_sync import get_local_version
        self.current_code_version = get_local_version()
        self.failed_sync_versions = {}
        
        import os
        os.environ["IS_WORKER"] = "true"
        
    def start(self):
        ensure_dependencies()
        logger.info(f"Worker {self.worker_id} starting (Current Code: {self.current_code_version})...")
        from distributed.log_sync import TCPLogHandler
        tcp_handler = TCPLogHandler(host=self.host, worker_id=self.worker_id)
        tcp_handler.setLevel(logging.INFO)
        root_logger = logging.getLogger()
        root_logger.addHandler(tcp_handler)
        logger.info(f"TCP log sync enabled to {self.host}:9872")
        
        # Register Graceful Signal Handlers
        import signal
        def handle_signal(signum, frame):
            logger.info(f"Received signal {signum}. Initiating graceful worker shutdown...")
            self.shutdown_requested = True
            
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
        
        cycle_failures = 0
        connect_failures = 0
        try:
            while not self.shutdown_requested:
                # Overall watchdog: if stuck in connect/cycle loops for > STARTUP_WATCHDOG, exit
                if time.time() - self._startup_time > _STARTUP_WATCHDOG and cycle_failures == 0 and connect_failures == 0:
                    pass  # At least one successful cycle resets the watchdog

                # 1. Hourly Git Update Check
                if time.time() - self.last_git_check > 3600:
                    self.last_git_check = time.time()
                    logger.info("Hourly check: Synchronizing code from master...")
                    try:
                        from distributed.code_sync import sync_code
                        sync_code(master_version="origin/main")
                    except Exception as sync_err:
                        logger.warning(f"Hourly git synchronization failed: {sync_err}")

                try:
                    if self.shutdown_requested:
                        break

                    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    conn.settimeout(_CONNECT_TIMEOUT)
                    try:
                        conn.connect((self.host, self.port))
                        connect_failures = 0
                    except Exception:
                        connect_failures += 1
                        conn.close()
                        if connect_failures >= _MAX_RETRIES:
                            logger.error(f"Master {self.host}:{self.port} unreachable after {_MAX_RETRIES} attempts. Giving up.")
                            break
                        _backoff_sleep(connect_failures)
                        continue

                    # Application-level handshake: verify this is really our master
                    conn.settimeout(_READ_TIMEOUT)
                    rfile = conn.makefile('r', encoding='utf-8')
                    try:
                        conn.sendall(b"HELLO\n")
                        hello_resp = rfile.readline()
                        if not hello_resp or not hello_resp.strip().startswith("WELCOME"):
                            logger.error(f"Bad handshake from {self.host}:{self.port} (got {hello_resp!r}). Not our master.")
                            conn.close()
                            connect_failures += 1
                            if connect_failures >= _MAX_RETRIES:
                                break
                            _backoff_sleep(connect_failures)
                            continue
                    except Exception:
                        conn.close()
                        connect_failures += 1
                        if connect_failures >= _MAX_RETRIES:
                            break
                        _backoff_sleep(connect_failures)
                        continue

                    # Handshake passed — we are talking to the real master
                    work_cycle_completed = False
                    while not self.shutdown_requested and not work_cycle_completed:
                        conn.sendall(b"GET_WORK\n")
                        data_line = rfile.readline()
                        if not data_line or self.shutdown_requested:
                            break
                        msg = data_line.strip()
                        if not msg:
                            break
                        order = WorkOrder.deserialize(msg)
                        logger.info(f"Received work order: {order.job_id} (Iteration {order.iteration})")
                        
                        # 2. Dynamic Git Synchronization on Code Version Mismatch
                        if order.code_version and order.code_version != self.current_code_version:
                            last_failed_time = self.failed_sync_versions.get(order.code_version, 0)
                            if time.time() - last_failed_time > 300:
                                logger.info(f"Detected code version mismatch (Local: {self.current_code_version}, Master: {order.code_version}). Triggering dynamic synchronization...")
                                try:
                                    from distributed.code_sync import sync_code, restart_process
                                    if hasattr(self.runner, '_executor') and self.runner._executor:
                                        self.runner._executor.shutdown(wait=False, cancel_futures=True)
                                        try:
                                            from factory.game_runner import GameRunner
                                            GameRunner._executor = None
                                        except Exception:
                                            pass
                                        self.runner._executor = None
                                    if sync_code(order.code_version):
                                        logger.info("Sync complete. Hot-restarting worker process...")
                                        restart_process()
                                    else:
                                        from distributed.code_sync import get_local_version
                                        current_head = get_local_version()
                                        if current_head and current_head == order.code_version:
                                            self.current_code_version = current_head
                                            logger.info(f"Code already up-to-date at {current_head}. Updated cached version without restart.")
                                        else:
                                            self.failed_sync_versions[order.code_version] = time.time()
                                except Exception as sync_err:
                                    logger.error(f"Dynamic synchronization failed: {sync_err}")
                                    self.failed_sync_versions[order.code_version] = time.time()
                        
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
                            cycle_failures = 0
                            connect_failures = 0
                            work_cycle_completed = True  # Return to outer loop for next work request
                        except Exception as e:
                            logger.error(f"Error running iteration: {e}")
                            break
                            
                    conn.close()
                    
                except (ConnectionRefusedError, socket.error) as e:
                    cycle_failures += 1
                    logger.warning(f"Connection error to {self.host}:{self.port} (attempt {cycle_failures}): {e}. Retrying...")
                    if cycle_failures >= _MAX_RETRIES:
                        logger.error(f"Master {self.host}:{self.port} unreachable after {_MAX_RETRIES} connect cycles.")
                        break
                    _backoff_sleep(cycle_failures)
                except Exception as e:
                    cycle_failures += 1
                    logger.error(f"Unexpected worker error (attempt {cycle_failures}): {e}. Retrying...")
                    if cycle_failures >= _MAX_RETRIES:
                        logger.error(f"Too many errors ({cycle_failures}). Giving up.")
                        break
                    _backoff_sleep(cycle_failures)
        finally:
            logger.info("Worker shutdown: cleaning up ProcessPoolExecutor child processes...")
            if hasattr(self.runner, '_executor') and self.runner._executor:
                self.runner._executor.shutdown(wait=False, cancel_futures=True)
                try:
                    from factory.game_runner import GameRunner
                    GameRunner._executor = None
                except Exception:
                    pass
                self.runner._executor = None
            logger.info("Worker client resources cleanly closed.")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    WorkerClient(host=host).start()
