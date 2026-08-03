import os
import logging

logger = logging.getLogger(__name__)
def _sigint_handler(signum, frame):
    print("\n[Ctrl+C] Interrupted by user. Exiting immediately...")
    os._exit(0)

