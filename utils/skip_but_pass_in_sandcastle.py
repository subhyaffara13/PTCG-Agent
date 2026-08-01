
def skip_but_pass_in_sandcastle(reason):
    """
    Similar to unittest.skip, however in the sandcastle environment it just
    "passes" the test instead to avoid creating tasks complaining about tests
    skipping continuously.
    """
    def decorator(func):
        if not IS_SANDCASTLE:
            func.__unittest_skip__ = True
            func.__unittest_skip_why__ = reason
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'Skipping {func.__name__} on sandcastle for following reason: {reason}', file=sys.stderr)
            return
        return wrapper

    return decorator

