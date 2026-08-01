
def skipIfTorchDynamo(msg="test doesn't currently work with dynamo"):
    """
    Usage:
    @skipIfTorchDynamo(msg)
    def test_blah(self):
        ...
    """
    if not isinstance(msg, str):
        raise AssertionError("Are you using skipIfTorchDynamo correctly?")

    def decorator(fn):
        if not isinstance(fn, type):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if TEST_WITH_TORCHDYNAMO:
                    raise unittest.SkipTest(msg)
                else:
                    fn(*args, **kwargs)
            return wrapper

        if not isinstance(fn, type):
            raise AssertionError(f"expected fn to be a type, got {type(fn)}")
        if TEST_WITH_TORCHDYNAMO:
            fn.__unittest_skip__ = True  # type: ignore[attr-defined]
            fn.__unittest_skip_why__ = msg  # type: ignore[attr-defined]

        return fn

    return decorator

