
def _validate_flavor(flavor):
    if flavor is None:
        flavor = "lxml", "bs4"
    elif isinstance(flavor, str):
        flavor = (flavor,)
    elif isinstance(flavor, abc.Iterable):
        if not all(isinstance(flav, str) for flav in flavor):
            raise TypeError(
                f"Object of type {type(flavor).__name__!r} "
                f"is not an iterable of strings"
            )
    else:
        msg = repr(flavor) if isinstance(flavor, str) else str(flavor)
        msg += " is not a valid flavor"
        raise ValueError(msg)

    flavor = tuple(flavor)
    valid_flavors = set(_valid_parsers)
    flavor_set = set(flavor)

    if not flavor_set & valid_flavors:
        raise ValueError(
            f"{_print_as_set(flavor_set)} is not a valid set of flavors, valid "
            f"flavors are {_print_as_set(valid_flavors)}"
        )
    return flavor

