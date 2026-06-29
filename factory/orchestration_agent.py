"""
factory/orchestration_agent.py
Top-level orchestration loop: launches training, monitors health, auto-submits.
"""
import sys
import os
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
    
    while True:
        try:
            listener = WorkerListener(interface_type="wifi")
            logger.info("[DISCOVERY] Listening for master...")
            master_ip, master_version = listener.listen_for_master()
            
            if master_ip:
                logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
                run_worker_loop(master_ip, master_version)
            else:
                logger.info("[ELECTION] No master found. Running election...")
                is_master, winner_ip = run_election(timeout=10)
                
                if is_master:
                    logger.info(f"[MASTER] Elected as master ({winner_ip}).")
                    run_master_loop()
                else:
                    logger.info(f"[WORKER] Master is {winner_ip}. Waiting for beacon...")
                    m_ip, m_version = listener.listen_for_master()
                    run_worker_loop(winner_ip, m_version)
        except Exception as e:
            logger.error(f"Critical error in Orchestration Agent loop: {e}")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
