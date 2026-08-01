
def merge_with(func, *dicts, **kwargs):
    """ Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
        dicts = dicts[0]
    factory = _get_factory(merge_with, kwargs)

    values = collections.defaultdict(lambda: [].append)
    for d in dicts:
        for k, v in d.items():
            values[k](v)

    result = factory()
    for k, v in values.items():
        result[k] = func(v.__self__)
    return result


def merge_with(func, *dicts, **kwargs):
    """Merge dictionaries and apply function to combined values

    A key may occur in more than one dict, and all values mapped from the key
    will be passed to the function as a list, such as func([val1, val2, ...]).

    >>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
    {1: 11, 2: 22}

    >>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
    {1: 1, 2: 2, 3: 30}

    See Also:
        merge
    """
    if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
        dicts = dicts[0]
    factory = _get_factory(merge_with, kwargs)

    result = factory()
    for d in dicts:
        for k, v in d.items():
            if k not in result:
                result[k] = [v]
            else:
                result[k].append(v)
    return valmap(func, result, factory)


def merge_with(func, d, *dicts, **kwargs):
    return toolz.merge_with(func, d, *dicts, **kwargs)

