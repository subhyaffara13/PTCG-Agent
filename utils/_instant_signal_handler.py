import logging
import os

def _instant_signal_handler(sig, frame):
    logging.info("Ctrl+C received. Terminating immediately...")
    os._exit(0)

