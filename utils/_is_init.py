
def _is_init(fn):
    return callable(fn) and fn.__name__ == "__init__"

