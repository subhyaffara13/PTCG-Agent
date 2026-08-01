
def requires_memory(free_bytes):
    """Decorator to skip a test if not enough memory is available"""
    import pytest

    def decorator(func):
        @wraps(func)
        def wrapper(*a, **kw):
            msg = check_free_memory(free_bytes)
            if msg is not None:
                pytest.skip(msg)

            try:
                return func(*a, **kw)
            except MemoryError:
                # Probably ran out of memory regardless: don't regard as failure
                pytest.xfail("MemoryError raised")

        return wrapper

    return decorator


def requires_memory(free_bytes):
    """Decorator to skip a test if not enough memory is available"""
    import pytest

    def decorator(func):
        @wraps(func)
        def wrapper(*a, **kw):
            msg = check_free_memory(free_bytes)
            if msg is not None:
                pytest.skip(msg)

            try:
                return func(*a, **kw)
            except MemoryError:
                # Probably ran out of memory regardless: don't regard as failure
                pytest.xfail("MemoryError raised")

        return wrapper

    return decorator

