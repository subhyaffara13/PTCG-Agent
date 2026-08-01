
def skipIfMPS(fn):
    sig = inspect.signature(fn)
    has_device_arg = "device" in sig.parameters

    if not has_device_arg:
        warnings.warn(
            f"skipIfMPS applied to {fn.__qualname__} which has no 'device' parameter. "
            "Consider using device-generic tests with instantiate_device_type_tests instead.",
            stacklevel=2,
        )

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if has_device_arg:
            # For device-generic tests, only skip when actually running on MPS
            slf = args[0] if args else None
            if slf is not None:
                device_type = getattr(slf, "device_type", None) or getattr(
                    slf, "device", None
                )
                if isinstance(device_type, str) and device_type == "mps":
                    raise unittest.SkipTest("test doesn't currently work with MPS")
        elif TEST_MPS:
            raise unittest.SkipTest("test doesn't currently work with MPS")
        return fn(*args, **kwargs)

    return wrapper

