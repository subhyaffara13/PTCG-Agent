
import sys
import os
import logging

def restart_process():
    logging.info("Restarting process to reload updated code and weights...")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        logging.error(f"os.execv failed: {e}. Exiting process.")
        sys.exit(0)

