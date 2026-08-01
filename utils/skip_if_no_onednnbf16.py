
def skipIfNoONEDNNBF16(fn):
    reason = "Quantized operations require BF16 support."
    if isinstance(fn, type):
        if not torch.ops.mkldnn._is_mkldnn_bf16_supported():
            fn.__unittest_skip__ = True
            fn.__unittest_skip_why__ = reason
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not torch.ops.mkldnn._is_mkldnn_bf16_supported():
            raise unittest.SkipTest(reason)
        else:
            fn(*args, **kwargs)

    return wrapper

