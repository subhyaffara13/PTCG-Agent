
def runWithoutCompiledAutograd(msg="test doesn't currently work with compiled autograd"):
    """
    Usage:
    @runWithoutCompiledAutograd(msg)
    def test_blah(self):
        ...
    """
    if not isinstance(msg, str):
        raise AssertionError(f"expected msg to be str, got {type(msg)}")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with torch._dynamo.compiled_autograd._disable():
                func(*args, **kwargs)
        return wrapper

    return decorator

