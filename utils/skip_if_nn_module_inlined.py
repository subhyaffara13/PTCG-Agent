
def skipIfNNModuleInlined(
    msg="test doesn't currently work with nn module inlining",
    condition=True,
):
    def decorator(fn):
        if not isinstance(fn, type):

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if condition:
                    raise unittest.SkipTest(msg)
                else:
                    fn(*args, **kwargs)

            return wrapper

        if not isinstance(fn, type):
            raise AssertionError(f"expected fn to be a type, got {type(fn)}")
        if condition:
            fn.__unittest_skip__ = True  # type: ignore[attr-defined]
            fn.__unittest_skip_why__ = msg  # type: ignore[attr-defined]

        return fn

    return decorator

