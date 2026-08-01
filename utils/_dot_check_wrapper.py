
def _dot_check_wrapper(fn):
    @wraps(fn)
    def wrapper(self, other):
        _dot_check(self, other)
        return fn(self, other)

    return wrapper

