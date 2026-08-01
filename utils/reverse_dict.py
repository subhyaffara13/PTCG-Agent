
def reverse_dict(d):
    """Reverses direction of dependence dict.

    >>> d = {"a": (1, 2), "b": (2, 3), "c": ()}
    >>> reverse_dict(d)  # doctest: +SKIP
    {1: ('a',), 2: ('a', 'b'), 3: ('b',)}

    .. note::
        dict order are not deterministic. As we iterate on the
        input dict, it make the output of this function depend on the
        dict order. So this function output order should be considered
        as undeterministic.
    """
    result = {}  # type: ignore[var-annotated]
    for key in d:
        for val in d[key]:
            # pyrefly: ignore [unsupported-operation]
            result[val] = result.get(val, ()) + (key,)
    return result


def reverse_dict(d):
    """Reverses direction of dependence dict.

    >>> d = {"a": (1, 2), "b": (2, 3), "c": ()}
    >>> reverse_dict(d)  # doctest: +SKIP
    {1: ('a',), 2: ('a', 'b'), 3: ('b',)}

    .. note::
        dict order are not deterministic. As we iterate on the
        input dict, it make the output of this function depend on the
        dict order. So this function output order should be considered
        as undeterministic.
    """
    result = OrderedDict()  # type: ignore[var-annotated]
    for key in d:
        for val in d[key]:
            # pyrefly: ignore [unsupported-operation]
            result[val] = result.get(val, ()) + (key,)
    return result


def reverse_dict(d):
    """Reverses direction of dependence dict

    >>> d = {'a': (1, 2), 'b': (2, 3), 'c':()}
    >>> reverse_dict(d)  # doctest: +SKIP
    {1: ('a',), 2: ('a', 'b'), 3: ('b',)}

    :note: dict order are not deterministic. As we iterate on the
        input dict, it make the output of this function depend on the
        dict order. So this function output order should be considered
        as undeterministic.

    """
    result = {}
    for key in d:
        for val in d[key]:
            result[val] = result.get(val, ()) + (key, )
    return result

