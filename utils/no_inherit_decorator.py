
def no_inherit_decorator(obj: T) -> T:
    """
    Identity decorator that prevents the modular converter from propagating its decorators to specific files.
    """
    return obj

