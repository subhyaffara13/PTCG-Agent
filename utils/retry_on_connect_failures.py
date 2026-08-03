import random
import time

def retry_on_connect_failures(func=None, connect_errors=(ADDRESS_IN_USE)):
    """Reruns a test if the test returns a RuntimeError and the exception
    contains one of the strings in connect_errors."""
    # This if block is executed when using this function as a decorator with arguments.
    if func is None:
        return partial(retry_on_connect_failures, connect_errors=connect_errors)

    @wraps(func)
    def wrapper(*args, **kwargs):
        n_retries = 10
        tries_remaining = n_retries
        while True:
            try:
                return func(*args, **kwargs)
            except RuntimeError as error:
                if any(connect_error in str(error) for connect_error in connect_errors):
                    tries_remaining -= 1
                    if tries_remaining == 0:
                        raise RuntimeError(f"Failing after {n_retries} retries with error: {str(error)}") from error
                    time.sleep(random.random())
                    continue
                raise
    return wrapper

