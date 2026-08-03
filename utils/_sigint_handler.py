import os

def _sigint_handler(signum, frame):
    print("\n[Ctrl+C] Interrupted by user. Exiting immediately...")
    os._exit(0)


def _sigint_handler(signum, frame):
    logger.info("[Ctrl+C] Interrupted by user. Terminating processes immediately...")
    try:
        cleanup()
    except Exception:
        pass
    os._exit(0)

