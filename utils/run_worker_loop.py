
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
    except KeyboardInterrupt:
        logger.info("[Ctrl+C] Worker loop interrupted by user. Exiting immediately...")
        import os
        os._exit(0)
    except Exception as e:
        logger.error(f"Worker client crashed: {e}. Restarting discovery...")
    finally:
        time.sleep(2)

