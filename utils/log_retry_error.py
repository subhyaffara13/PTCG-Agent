import logging

def log_retry_error(details):
    exception = details.get("exception")
    tries = details.get("tries")
    if exception:
        logging.error(f"Confident AI Error: {exception}. Retrying: {tries} time(s)...")
    else:
        logging.error(f"Retrying: {tries} time(s)...")

