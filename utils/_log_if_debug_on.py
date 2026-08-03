import functools

def _log_if_debug_on(meth):
    """
    Wrap `RendererPS` method *meth* to emit a PS comment with the method name,
    if the global flag `debugPS` is set.
    """
    @functools.wraps(meth)
    def wrapper(self, *args, **kwargs):
        if debugPS:
            self._pswriter.write(f"% {meth.__name__}\n")
        return meth(self, *args, **kwargs)

    return wrapper

