
def torch_only_method(fn: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if not is_torch_available():
            raise ImportError("You need to install pytorch to use this method or class")
        else:
            return fn(*args, **kwargs)

    return wrapper

