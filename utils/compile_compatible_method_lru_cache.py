
def compile_compatible_method_lru_cache(*lru_args, **lru_kwargs):
    """
    LRU cache decorator from standard functools library, but with a workaround to disable
    caching when torchdynamo is compiling. Expected to work with class methods.
    """

    def decorator(func):
        func_with_cache = lru_cache(*lru_args, **lru_kwargs)(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_torchdynamo_compiling():
                return func(*args, **kwargs)
            else:
                return func_with_cache(*args, **kwargs)

        return wrapper

    return decorator

