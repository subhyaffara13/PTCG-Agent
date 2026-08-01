
def async_gen_wrapper(func, obj=None):
    """Given a async generator, make so can be called in blocking contexts"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = obj or args[0]
        gen = func(*args, **kwargs)
        while True:
            try:
                yield sync(self.loop, gen.__anext__)
            except StopAsyncIteration:
                break

    return wrapper

