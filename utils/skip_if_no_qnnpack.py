
def skipIfNoQNNPACK(fn):
    reason = "Quantized operations require QNNPACK."
    if isinstance(fn, type):
        if "qnnpack" not in torch.backends.quantized.supported_engines:
            fn.__unittest_skip__ = True
            fn.__unittest_skip_why__ = reason
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if "qnnpack" not in torch.backends.quantized.supported_engines:
            raise unittest.SkipTest(reason)
        else:
            fn(*args, **kwargs)

    return wrapper

