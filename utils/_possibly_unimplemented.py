
def _possibly_unimplemented(cls, require=True):
    """
    Construct a class that either runs tests as usual (require=True),
    or each method skips if it encounters a common error.
    """
    if require:
        return cls
    else:
        def wrap(fc):
            @functools.wraps(fc)
            def wrapper(*a, **kw):
                try:
                    return fc(*a, **kw)
                except (NotImplementedError, TypeError, ValueError,
                        IndexError, AttributeError):
                    raise pytest.skip("feature not implemented")

            return wrapper

        new_dict = dict(cls.__dict__)
        for name, func in cls.__dict__.items():
            if name.startswith('test_'):
                new_dict[name] = wrap(func)
        return type(cls.__name__ + "NotImplemented",
                    cls.__bases__,
                    new_dict)

