
def skipIfNoFBGEMM(fn):
    reason = "Quantized operations require FBGEMM. FBGEMM is only optimized for CPUs with instruction set support AVX2 or newer."
    if isinstance(fn, type):
        if "fbgemm" not in torch.backends.quantized.supported_engines:
            fn.__unittest_skip__ = True
            fn.__unittest_skip_why__ = reason
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if "fbgemm" not in torch.backends.quantized.supported_engines:
            raise unittest.SkipTest(reason)
        else:
            fn(*args, **kwargs)

    return wrapper

