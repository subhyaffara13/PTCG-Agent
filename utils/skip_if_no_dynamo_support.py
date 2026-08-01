
def skipIfNoDynamoSupport(fn):
    reason = "dynamo doesn't support."
    if isinstance(fn, type):
        if not torchdynamo.is_dynamo_supported():
            fn.__unittest_skip__ = True
            fn.__unittest_skip_why__ = reason
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not torchdynamo.is_dynamo_supported():
            raise unittest.SkipTest(reason)
        else:
            fn(*args, **kwargs)

    return wrapper

