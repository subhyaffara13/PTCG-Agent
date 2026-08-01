
def _check_other_SISO(func):
    def wrapper(*args, **kwargs):
        if not isinstance(args[-1], SISOLinearTimeInvariant):
            return NotImplemented
        else:
            return func(*args, **kwargs)
    return wrapper

