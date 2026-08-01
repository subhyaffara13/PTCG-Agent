
def cycler(arg: Cycler[K, V]) -> Cycler[K, V]:
    ...


def cycler(**kwargs: Iterable[V]) -> Cycler[str, V]:
    ...


def cycler(label: K, itr: Iterable[V]) -> Cycler[K, V]:
    ...


def cycler(*args, **kwargs):
    """
    Create a new `Cycler` object from a single positional argument,
    a pair of positional arguments, or the combination of keyword arguments.

    cycler(arg)
    cycler(label1=itr1[, label2=iter2[, ...]])
    cycler(label, itr)

    Form 1 simply copies a given `Cycler` object.

    Form 2 composes a `Cycler` as an inner product of the
    pairs of keyword arguments. In other words, all of the
    iterables are cycled simultaneously, as if through zip().

    Form 3 creates a `Cycler` from a label and an iterable.
    This is useful for when the label cannot be a keyword argument
    (e.g., an integer or a name that has a space in it).

    Parameters
    ----------
    arg : Cycler
        Copy constructor for Cycler (does a shallow copy of iterables).
    label : name
        The property key. In the 2-arg form of the function,
        the label can be any hashable object. In the keyword argument
        form of the function, it must be a valid python identifier.
    itr : iterable
        Finite length iterable of the property values.
        Can be a single-property `Cycler` that would
        be like a key change, but as a shallow copy.

    Returns
    -------
    cycler : Cycler
        New `Cycler` for the given property

    """
    if args and kwargs:
        raise TypeError(
            "cycler() can only accept positional OR keyword arguments -- not both."
        )

    if len(args) == 1:
        if not isinstance(args[0], Cycler):
            raise TypeError(
                "If only one positional argument given, it must "
                "be a Cycler instance."
            )
        return Cycler(args[0])
    elif len(args) == 2:
        return _cycler(*args)
    elif len(args) > 2:
        raise TypeError(
            "Only a single Cycler can be accepted as the lone "
            "positional argument. Use keyword arguments instead."
        )

    if kwargs:
        return reduce(add, (_cycler(k, v) for k, v in kwargs.items()))

    raise TypeError("Must have at least a positional OR keyword arguments")


def cycler(*args, **kwargs):
    """
    Create a `~cycler.Cycler` object much like :func:`cycler.cycler`,
    but includes input validation.

    Call signatures::

      cycler(cycler)
      cycler(label=values, label2=values2, ...)
      cycler(label, values)

    Form 1 copies a given `~cycler.Cycler` object.

    Form 2 creates a `~cycler.Cycler` which cycles over one or more
    properties simultaneously. If multiple properties are given, their
    value lists must have the same length.

    Form 3 creates a `~cycler.Cycler` for a single property. This form
    exists for compatibility with the original cycler. Its use is
    discouraged in favor of the kwarg form, i.e. ``cycler(label=values)``.

    Parameters
    ----------
    cycler : Cycler
        Copy constructor for Cycler.

    label : str
        The property key. Must be a valid `.Artist` property.
        For example, 'color' or 'linestyle'. Aliases are allowed,
        such as 'c' for 'color' and 'lw' for 'linewidth'.

    values : iterable
        Finite-length iterable of the property values. These values
        are validated and will raise a ValueError if invalid.

    Returns
    -------
    Cycler
        A new :class:`~cycler.Cycler` for the given properties.

    Examples
    --------
    Creating a cycler for a single property:

    >>> c = cycler(color=['red', 'green', 'blue'])

    Creating a cycler for simultaneously cycling over multiple properties
    (e.g. red circle, green plus, blue cross):

    >>> c = cycler(color=['red', 'green', 'blue'],
    ...            marker=['o', '+', 'x'])

    """
    if args and kwargs:
        raise TypeError("cycler() can only accept positional OR keyword "
                        "arguments -- not both.")
    elif not args and not kwargs:
        raise TypeError("cycler() must have positional OR keyword arguments")

    if len(args) == 1:
        if not isinstance(args[0], Cycler):
            raise TypeError("If only one positional argument given, it must "
                            "be a Cycler instance.")
        return validate_cycler(args[0])
    elif len(args) == 2:
        pairs = [(args[0], args[1])]
    elif len(args) > 2:
        raise _api.nargs_error('cycler', '0-2', len(args))
    else:
        pairs = kwargs.items()

    validated = []
    for prop, vals in pairs:
        norm_prop = _prop_aliases.get(prop, prop)
        validator = _prop_validators.get(norm_prop, None)
        if validator is None:
            raise TypeError("Unknown artist property: %s" % prop)
        vals = validator(vals)
        # We will normalize the property names as well to reduce
        # the amount of alias handling code elsewhere.
        validated.append((norm_prop, vals))

    return reduce(operator.add, (ccycler(k, v) for k, v in validated))

