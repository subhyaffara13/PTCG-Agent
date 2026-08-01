
def _exception_logger(func: Callable[_P, _T]) -> Callable[_P, _T]:
    @functools.wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        try:
            return func(*args, **kwargs)
        except Exception as error:
            msg_dict = _get_msg_dict(func.__name__, *args, **kwargs)
            msg_dict["error"] = f"{error}"
            _c10d_logger.debug(msg_dict)
            raise

    return wrapper

