import functools
import time

def retry_error_partial_copy(fun):
    """Workaround for https://github.com/giampaolo/psutil/issues/875.
    See: https://stackoverflow.com/questions/4457745#4457745.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        delay = 0.0001
        times = 33
        for _ in range(times):  # retries for roughly 1 second
            try:
                return fun(self, *args, **kwargs)
            except OSError as _:
                err = _
                if err.winerror == ERROR_PARTIAL_COPY:
                    time.sleep(delay)
                    delay = min(delay * 2, 0.04)
                    continue
                raise
        msg = (
            f"{fun} retried {times} times, converted to AccessDenied as it's "
            f"still returning {err}"
        )
        raise AccessDenied(pid=self.pid, name=self._name, msg=msg)

    return wrapper

