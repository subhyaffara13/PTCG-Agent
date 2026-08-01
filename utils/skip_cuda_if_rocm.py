
def skipCUDAIfRocm(func=None, *, msg="test doesn't currently work on the ROCm stack"):
    def dec_fn(fn):
        reason = f"skipCUDAIfRocm: {msg}"
        return skipCUDAIf(TEST_WITH_ROCM, reason=reason)(fn)

    if func:
        return dec_fn(func)
    return dec_fn

