
def runOnRocmArch(arch: tuple[str, ...]):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if TEST_WITH_ROCM and not isRocmArchAnyOf(arch):
                reason = f"skipIfRocm: test only runs on {arch}"
                raise unittest.SkipTest(reason)
            return fn(self, *args, **kwargs)
        return wrap_fn
    return dec_fn

