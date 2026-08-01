
def _sleep_for_timeout(timeout: Union[float, str, httpx.Timeout]):
    if isinstance(timeout, float):
        time.sleep(timeout)
    elif isinstance(timeout, str):
        time.sleep(float(timeout))
    elif isinstance(timeout, httpx.Timeout) and timeout.connect is not None:
        time.sleep(timeout.connect)

