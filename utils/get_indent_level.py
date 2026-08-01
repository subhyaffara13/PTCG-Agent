
def get_indent_level(func):
    # Use this instead of `inspect.getsource(func)` as getsource can be very slow
    return (len(func.__qualname__.split(".")) - 1) * 4

