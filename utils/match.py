
def match(pattern, string, flags=0, pos=None, endpos=None, partial=False,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Try to apply the pattern at the start of the string, returning a match
    object, or None if no match was found."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.match(string, pos, endpos, concurrent, partial, timeout)


def match(*signature, **kwargs):
    namespace = kwargs.get("namespace", global_namespace)
    dispatcher = kwargs.get("Dispatcher", Dispatcher)

    def _(func):
        name = func.__name__

        if name not in namespace:
            namespace[name] = dispatcher(name)
        d = namespace[name]

        d.add(signature, func)

        return d

    return _

