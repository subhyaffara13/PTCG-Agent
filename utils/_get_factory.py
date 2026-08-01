
def _get_factory(f, kwargs):
    factory = kwargs.pop('factory', dict)
    if kwargs:
        raise TypeError("{}() got an unexpected keyword argument "
                        "'{}'".format(f.__name__, kwargs.popitem()[0]))
    return factory


def _get_factory(f, kwargs):
    factory = kwargs.pop("factory", dict)
    if kwargs:
        raise TypeError(
            f"{f.__name__}() got an unexpected keyword argument '{kwargs.popitem()[0]}'"
        )
    return factory

