
def current_default_interpreter_limiter() -> CapacityLimiter:
    """
    Return the capacity limiter used by default to limit the number of concurrently
    running subinterpreters.

    Defaults to the number of CPU cores.

    :return: a capacity limiter object

    """
    try:
        return _default_interpreter_limiter.get()
    except LookupError:
        limiter = CapacityLimiter(os.cpu_count() or DEFAULT_CPU_COUNT)
        _default_interpreter_limiter.set(limiter)
        return limiter

