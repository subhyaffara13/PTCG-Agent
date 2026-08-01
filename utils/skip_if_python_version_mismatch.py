
def skipIfPythonVersionMismatch(predicate):
    vi = sys.version_info

    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if predicate(vi.major, vi.minor, vi.micro):
                return fn(self, *args, **kwargs)
            else:
                raise unittest.SkipTest("Python version mismatch")
        return wrap_fn
    return dec_fn

