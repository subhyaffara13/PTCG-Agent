
def do_format(value: str, *args: t.Any, **kwargs: t.Any) -> str:
    """Apply the given values to a `printf-style`_ format string, like
    ``string % values``.

    .. sourcecode:: jinja

        {{ "%s, %s!"|format(greeting, name) }}
        Hello, World!

    In most cases it should be more convenient and efficient to use the
    ``%`` operator or :meth:`str.format`.

    .. code-block:: text

        {{ "%s, %s!" % (greeting, name) }}
        {{ "{}, {}!".format(greeting, name) }}

    .. _printf-style: https://docs.python.org/library/stdtypes.html
        #printf-style-string-formatting
    """
    if args and kwargs:
        raise FilterArgumentError(
            "can't handle positional and keyword arguments at the same time"
        )

    return soft_str(value) % (kwargs or args)

