
def get_callable_name(obj):
    # typical case has name
    if hasattr(obj, "__name__"):
        return obj.__name__
    # some objects don't; could recurse
    if isinstance(obj, partial):
        return get_callable_name(obj.func)
    # fall back to class name
    if callable(obj):
        return type(obj).__name__
    # everything failed (probably because the argument
    # wasn't actually callable); we return None
    # instead of the empty string in this case to allow
    # distinguishing between no name and a name of ''
    return None


def get_callable_name(func: Callable, override: object = None) -> str:
    if override is not None:
        return str(override)

    module = getattr(func, "__module__", None)
    qualname = getattr(func, "__qualname__", None)
    return ".".join([x for x in (module, qualname) if x])

