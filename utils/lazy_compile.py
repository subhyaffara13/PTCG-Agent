import functools

def lazy_compile(**compile_kwargs):
    """Lazily wrap a function with torch.compile on the first call

    This avoids eagerly importing dynamo.
    """

    def decorate_fn(fn):
        @functools.wraps(fn)
        def compile_hook(*args, **kwargs):
            compiled_fn = torch.compile(fn, **compile_kwargs)
            globals()[fn.__name__] = functools.wraps(fn)(compiled_fn)
            return compiled_fn(*args, **kwargs)

        return compile_hook

    return decorate_fn

