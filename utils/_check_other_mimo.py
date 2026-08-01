
def _check_other_MIMO(func):
    def wrapper(*args, **kwargs):
        if not isinstance(args[-1], MIMOLinearTimeInvariant):
            return NotImplemented
        else:
            return func(*args, **kwargs)
    return wrapper

