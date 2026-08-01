import time
import sys
import subprocess
import logging
from utils.script_log_path import script_log_path

logger = logging.getLogger("orchestration_agent")

def launch_processes(scripts: list) -> list:
    processes = []
    for i, script in enumerate(scripts):
        if i > 0:
            time.sleep(15)
        log_path = script_log_path(script)
        try:
            f = open(log_path, "a", encoding="utf-8")
            p = subprocess.Popen([sys.executable, script], stdout=f, stderr=f)
            processes.append((p, f))
            logger.info(f"Started: {script} (PID {p.pid}) -> {log_path}")
        except Exception as e:
            logger.error(f"Failed to start {script}: {e}")
            processes.append((None, None))
    return processes
