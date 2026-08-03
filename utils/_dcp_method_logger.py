import functools
import time
from typing import Any, Callable

def _dcp_method_logger(
    log_exceptions: bool = False, **wrapper_kwargs: Any
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:  # pyre-ignore
    """This method decorator logs the start, end, and exception of wrapped events."""

    def decorator(func: Callable[_P, _T]):
        @functools.wraps(func)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            msg_dict = _get_msg_dict(
                func.__name__, *args, **{**wrapper_kwargs, **kwargs}
            )

            # log start event
            msg_dict["event"] = "start"
            t0 = time.time_ns()
            msg_dict["time"] = t0
            msg_dict["log_exceptions"] = log_exceptions
            _dcp_logger.debug(msg_dict)

            # exceptions
            try:
                result = func(*args, **kwargs)
            except BaseException as error:
                if log_exceptions:
                    msg_dict["event"] = "exception"
                    msg_dict["error"] = f"{error}"
                    msg_dict["time"] = time.time_ns()
                    _dcp_logger.error(msg_dict)
                raise

            # end event
            msg_dict["event"] = "end"
            t1 = time.time_ns()
            msg_dict["time"] = time.time_ns()
            msg_dict["times_spent"] = t1 - t0
            _dcp_logger.debug(msg_dict)

            return result

        return wrapper

    return decorator

