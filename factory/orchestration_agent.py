"""
factory/orchestration_agent.py
Top-level orchestration loop: launches training, monitors health, auto-submits.
"""
import sys
import os

# Fix path for os.execv restarts which launch as script instead of module
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import time
import subprocess
import json
import logging
from factory.orchestration_agent_helpers import (
    auto_submit_if_ready, run_analytics_check, get_training_scripts
)
from factory.orchestration_process import (
    launch_processes, monitor_and_restart, cleanup, script_log_path
)

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("orchestration_agent")
logger.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh = logging.FileHandler("logs/orchestration_agent.log", mode="a", encoding="utf-8")
fh.setFormatter(fmt)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(fmt)
logger.addHandler(sh)

import os
ENABLE_DISTRIBUTED = os.environ.get("ENABLE_DISTRIBUTED") == "1"


def main():
    import sys
    if "--force-master" in sys.argv:
        logger.info("[OVERRIDE] --force-master flag detected. Bypassing discovery and forcing Master Mode.")
        from factory.orchestrator_master import run_master_loop
        while True:
            try:
                run_master_loop()
            except Exception as e:
                logger.error(f"Master loop crashed: {e}")
        return

    logger.info("Orchestration Agent (Auto-Discovery Mode) started.")
    from distributed.discovery import WorkerListener
    from distributed.election import run_election
    from factory.orchestrator_master import run_master_loop
    from factory.orchestrator_worker import run_worker_loop
    
    last_seen_master_time = None
    last_known_master_ip = None
    
    while True:
        try:
            listener = WorkerListener(interface_type="wifi")
            logger.info("[DISCOVERY] Listening for master...")
            master_ip, master_version = listener.listen_for_master()
            
            if master_ip:
                logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
                last_seen_master_time = time.time()
                last_known_master_ip = master_ip
                
                try:
                    from distributed.code_sync import sync_code, restart_process
                    if master_version and sync_code(master_version):
                        restart_process()
                except Exception as sync_e:
                    logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                    
                run_worker_loop(master_ip, master_version)
            else:
                grace_period = 300  # 5 minutes
                if last_known_master_ip and last_seen_master_time and (time.time() - last_seen_master_time < grace_period):
                    logger.info(f"[DISCOVERY] Master beacons temporarily missing. Last seen master: {last_known_master_ip}. Retrying direct connect...")
                    try:
                        run_worker_loop(last_known_master_ip, None)
                    except Exception as loop_err:
                        logger.warning(f"Failed direct reconnect: {loop_err}")
                    time.sleep(5)
                else:
                    logger.info("[ELECTION] No master found and grace period expired. Running election...")
                    is_master, winner_ip = run_election(timeout=10)
                    
                    if is_master:
                        logger.info(f"[MASTER] Elected as master ({winner_ip}).")
                        run_master_loop()
                    else:
                        logger.info(f"[WORKER] Master is {winner_ip}. Waiting for beacon...")
                        m_ip, m_version = listener.listen_for_master()
                        
                        try:
                            from distributed.code_sync import sync_code, restart_process
                            if m_version and sync_code(m_version):
                                restart_process()
                        except Exception as sync_e:
                            logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                            
                        run_worker_loop(winner_ip, m_version)
        except Exception as e:
            logger.error(f"Critical error in Orchestration Agent loop: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
