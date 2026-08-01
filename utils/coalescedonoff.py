
def coalescedonoff(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        f(self, *args, **kwargs, coalesced=True)
        f(self, *args, **kwargs, coalesced=False)
    return wrapped

