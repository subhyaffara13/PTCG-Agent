
def get_formatter_by_name(_alias, **options):
    """
    Return an instance of a :class:`.Formatter` subclass that has `alias` in its
    aliases list. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter with that
    alias is found.
    """
    cls = find_formatter_class(_alias)
    if cls is None:
        raise ClassNotFound(f"no formatter found for name {_alias!r}")
    return cls(**options)


def get_formatter_by_name(_alias, **options):
    """
    Return an instance of a :class:`.Formatter` subclass that has `alias` in its
    aliases list. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter with that
    alias is found.
    """
    cls = find_formatter_class(_alias)
    if cls is None:
        raise ClassNotFound(f"no formatter found for name {_alias!r}")
    return cls(**options)

