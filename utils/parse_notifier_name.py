
def parse_notifier_name(names: Sentinel | str | t.Iterable[Sentinel | str]) -> t.Iterable[t.Any]:
    """Convert the name argument to a list of names.

    Examples
    --------
    >>> parse_notifier_name([])
    [traitlets.All]
    >>> parse_notifier_name("a")
    ['a']
    >>> parse_notifier_name(["a", "b"])
    ['a', 'b']
    >>> parse_notifier_name(All)
    [traitlets.All]
    """
    if names is All or isinstance(names, str):
        return [names]
    elif isinstance(names, Sentinel):
        raise TypeError("`names` must be either `All`, a str, or a list of strs.")
    else:
        if not names or All in names:
            return [All]
        for n in names:
            if not isinstance(n, str):
                raise TypeError(f"names must be strings, not {type(n).__name__}({n!r})")
        return names

