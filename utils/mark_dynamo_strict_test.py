
def markDynamoStrictTest(cls_or_func=None, nopython=False):
    """
    Marks the test as 'strict'. In strict mode, we reset before and after the
    test, and run without suppress errors.

    Args:
    - nopython: if we should run torch._dynamo.optimize with nopython={True/False}.
    """
    def decorator(cls_or_func):
        if inspect.isclass(cls_or_func):
            cls_or_func.dynamo_strict = True
            cls_or_func.dynamo_strict_nopython = nopython
            return cls_or_func

        fn = cls_or_func

        @wraps(fn)
        def wrapper(*args, **kwargs):
            torch._dynamo.reset()
            with unittest.mock.patch("torch._dynamo.config.suppress_errors", False):
                fn(*args, **kwargs)
            torch._dynamo.reset()
        return wrapper

    if cls_or_func is None:
        return decorator
    else:
        return decorator(cls_or_func)

