
def skipCUDAIfVersionLessThan(versions: tuple[int, int] | None = None):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            version = _get_torch_cuda_version()
            if version == (0, 0):  # cpu or rocm
                return fn(self, *args, **kwargs)
            if version < versions:
                reason = f"test skipped for CUDA versions < {version}"
                raise unittest.SkipTest(reason)
            return fn(self, *args, **kwargs)

        return wrap_fn

    return dec_fn

