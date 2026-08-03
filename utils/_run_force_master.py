import time

def _run_force_master():
    from factory.orchestrator_master import run_master_loop
    logger.info("[OVERRIDE] Force Master Mode detected.")
    while True:
        try: run_master_loop(enable_distributed=True)
        except KeyboardInterrupt: logger.info("Force Master loop terminated."); break
        except Exception as e: logger.error(f"Master loop crashed: {e}"); time.sleep(5)

