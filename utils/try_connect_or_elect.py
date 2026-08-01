
def try_connect_or_elect(listener, last_seen_master_time, last_known_master_ip, run_master_loop, run_worker_loop, run_election):
    master_ip, master_version = listener.listen_for_master()
    if master_ip:
        logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
        from distributed.code_sync import sync_code, restart_process
        if master_version and sync_code(master_version): restart_process()
        run_worker_loop(master_ip, master_version)
    else:
        _handle_no_master(listener, last_seen_master_time, last_known_master_ip, run_master_loop, run_worker_loop, run_election)

