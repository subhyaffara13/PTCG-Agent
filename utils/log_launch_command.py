import sys

def log_launch_command():
    """Logs the command used to launch the script."""
    command = " ".join(sys.argv)
    logger.info(f"Launch command: {command}")

