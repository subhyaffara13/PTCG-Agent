
def largeTensorTest(size, device=None, inductor=TEST_WITH_TORCHINDUCTOR):
    """Skip test if the device has insufficient memory to run the test

    size may be a number of bytes, a string of the form "N GB", or a callable

    If the test is a device generic test, available memory on the primary device will be checked.
    It can also be overridden by the optional `device=` argument.
    In other tests, the `device=` argument needs to be specified.
    """
    if isinstance(size, str):
        if not size.endswith(("GB", "gb")):
            raise AssertionError(f"only bytes or GB supported, got {size!r}")
        size = 1024**3 * int(size[:-2])

    def inner(fn):
        @wraps(fn)
        def dep_fn(self, *args, **kwargs):
            size_bytes: int = size(self, *args, **kwargs) if callable(size) else size
            _device = device
            if _device is None:
                if hasattr(self, "get_primary_device"):
                    _device = self.get_primary_device()
                else:
                    _device = self.device

            # If this is running with GPU cpp_wrapper, the autotuning step will generate
            # an additional array of the same size as the input.
            if inductor and torch._inductor.config.cpp_wrapper and _device != "cpu":
                size_bytes *= 2
            if not _has_sufficient_memory(_device, size_bytes):
                raise unittest.SkipTest(f"Insufficient {_device} memory")

            return fn(self, *args, **kwargs)

        return dep_fn

    return inner

