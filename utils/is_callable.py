
def is_callable():
    """
    A validator that raises a `attrs.exceptions.NotCallableError` if the
    initializer is called with a value for this particular attribute that is
    not callable.

    .. versionadded:: 19.1.0

    Raises:
        attrs.exceptions.NotCallableError:
            With a human readable error message containing the attribute
            (`attrs.Attribute`) name, and the value it got.
    """
    return _IsCallableValidator()


def is_callable(tp: Any, /) -> bool:
    """Return whether the provided argument is a `Callable`, parametrized or not.

    ```python {test="skip" lint="skip"}
    is_callable(Callable[[int], str])
    #> True
    is_callable(typing.Callable)
    #> True
    is_callable(collections.abc.Callable)
    #> True
    ```
    """
    # `get_origin` is documented as normalizing any typing-module aliases to `collections` classes,
    # hence the second check:
    return tp is collections.abc.Callable or get_origin(tp) is collections.abc.Callable


def is_callable(obj: object) -> bool:
    """

    Parameters
    ----------
    `obj` - the object to be checked

    Returns
    -------
    validator - returns True if object is callable
        raises ValueError otherwise.

    """
    if not callable(obj):
        raise ValueError("Value must be a callable")
    return True

