import time
import logging
logger = logging.getLogger("orchestration_agent")

def _run_force_master():
    from factory.orchestrator_master import run_master_loop
    logger.info("[OVERRIDE] Force Master Mode detected.")
    while True:
        try: run_master_loop(enable_distributed=True)
        except KeyboardInterrupt: logger.info("Force Master loop terminated."); break
        except Exception as e: logger.error(f"Master loop crashed: {e}"); time.sleep(5)

def _handle_no_master(listener, last_seen_master_time, last_known_master_ip, run_master_loop, run_worker_loop, run_election):
    grace_period = 300
    if last_known_master_ip and last_seen_master_time and (time.time() - last_seen_master_time < grace_period):
        logger.info(f"[DISCOVERY] Master temporarily missing. Retrying direct connect...")
        try: run_worker_loop(last_known_master_ip, None)
        except Exception: pass
        time.sleep(5)
    else:
        logger.info("[ELECTION] No master found. Running election...")
        is_master, winner_ip = run_election(timeout=10)
        if is_master:
            logger.info(f"[MASTER] Elected as master."); run_master_loop(enable_distributed=True)
        else:
            logger.info(f"[WORKER] Master is {winner_ip}.")
            m_ip, m_version = listener.listen_for_master()
            try:
                from distributed.code_sync import sync_code, restart_process
                if m_version and sync_code(m_version): restart_process()
            except Exception: pass
            run_worker_loop(winner_ip, m_version)

def try_connect_or_elect(listener, last_seen_master_time, last_known_master_ip, run_master_loop, run_worker_loop, run_election):
    master_ip, master_version = listener.listen_for_master()
    if master_ip:
        logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
        from distributed.code_sync import sync_code, restart_process
        if master_version and sync_code(master_version): restart_process()
        run_worker_loop(master_ip, master_version)
    else:
        _handle_no_master(listener, last_seen_master_time, last_known_master_ip, run_master_loop, run_worker_loop, run_election)
