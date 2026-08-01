
def do_max(
    environment: "Environment",
    value: "t.Iterable[V]",
    case_sensitive: bool = False,
    attribute: t.Optional[t.Union[str, int]] = None,
) -> "t.Union[V, Undefined]":
    """Return the largest item from the sequence.

    .. sourcecode:: jinja

        {{ [1, 2, 3]|max }}
            -> 3

    :param case_sensitive: Treat upper and lower case strings as distinct.
    :param attribute: Get the object with the max value of this attribute.
    """
    return _min_or_max(environment, value, max, case_sensitive, attribute)

