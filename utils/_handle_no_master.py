import time

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

