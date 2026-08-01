
def disableMkldnn(fn):
    @wraps(fn)
    def disable_mkldnn(self, *args, **kwargs):
        if torch.backends.mkldnn.is_available():
            with torch.backends.mkldnn.flags(enabled=False):
                return fn(self, *args, **kwargs)
        return fn(self, *args, **kwargs)

    return disable_mkldnn

