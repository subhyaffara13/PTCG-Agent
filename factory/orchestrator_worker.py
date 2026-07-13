import time
import warnings
import logging
from distributed.worker_client import WorkerClient

logger = logging.getLogger("orchestration_agent")

# Suppress noisy litellm model cost map warning (harmless, model name not in cost registry)
warnings.filterwarnings("ignore", message=".*not in built-in cost map.*")

def run_worker_loop(master_ip: str, master_version: str | None):
    logger.info(f"Orchestration Agent (Worker Mode) started. Syncing to {master_version}...")
    from distributed.code_sync import sync_code, restart_process
    if master_version:
        if sync_code(master_version):
            restart_process()

    client = WorkerClient(host=master_ip)
    try:
        client.start()
    except ConnectionError as e:
        logger.warning(f"Connection to master lost: {e}. Restarting discovery...")
    except Exception as e:
        logger.error(f"Worker client crashed: {e}. Restarting discovery...")
    finally:
        time.sleep(2)
