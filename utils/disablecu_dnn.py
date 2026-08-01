
def disablecuDNN(fn):
    @wraps(fn)
    def disable_cudnn(self, *args, **kwargs):
        if self.device_type == "cuda" and self.has_cudnn():
            with torch.backends.cudnn.flags(enabled=False):
                return fn(self, *args, **kwargs)
        return fn(self, *args, **kwargs)

    return disable_cudnn

