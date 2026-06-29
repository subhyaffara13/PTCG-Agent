import time
import logging
from distributed.worker_client import WorkerClient

logger = logging.getLogger("orchestration_agent")

def run_worker_loop(master_ip: str, master_version: str):
    logger.info(f"Orchestration Agent (Worker Mode) started. Syncing to {master_version}...")
    from distributed.code_sync import sync_code
    if master_version:
        sync_code(master_version)

    client = WorkerClient(host=master_ip)
    try:
        client.start()
    except ConnectionError as e:
        logger.warning(f"Connection to master lost: {e}. Restarting discovery...")
    except Exception as e:
        logger.error(f"Worker client crashed: {e}. Restarting discovery...")
    finally:
        time.sleep(2)
