
def restart_process():
    import sys
    import os
    logging.info("Restarting process to reload updated code and weights...")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        logging.error(f"os.execv failed: {e}. Exiting process.")
        sys.exit(0)

