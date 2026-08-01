
def skipDeviceIf(cond, msg, *, device):
    if cond:

        def decorate_fn(fn):
            @functools.wraps(fn)
            def inner(self, *args, **kwargs):
                if not hasattr(self, "device"):
                    warn_msg = (
                        "Expect the test class to have attribute device but not found. "
                    )
                    if hasattr(self, "device_type"):
                        warn_msg += "Consider using the skip device decorators in common_device_type.py"
                    log.warning(warn_msg)
                if self.device == device:
                    raise unittest.SkipTest(msg)
                return fn(self, *args, **kwargs)

            return inner

    else:

        def decorate_fn(fn):
            return fn

    return decorate_fn

