import time


def _backoff_sleep(attempt: int):
    """Exponential backoff: 1, 2, 4, 8, 16, 30, 30, ... seconds."""
    delay = min(30, 2 ** attempt)
    time.sleep(delay)
