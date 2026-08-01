
def public(obj: T) -> T:
    """
    Append ``obj``'s name to global ``__all__`` variable (call site).

    By using this decorator on functions or classes you achieve the same goal
    as by filling ``__all__`` variables manually, you just do not have to repeat
    yourself (object's name). You also know if object is public at definition
    site, not at some random location (where ``__all__`` was set).

    Note that in multiple decorator setup (in almost all cases) ``@public``
    decorator must be applied before any other decorators, because it relies
    on the pointer to object's global namespace. If you apply other decorators
    first, ``@public`` may end up modifying the wrong namespace.

    Examples
    ========

    >>> from sympy.utilities.decorator import public

    >>> __all__ # noqa: F821
    Traceback (most recent call last):
    ...
    NameError: name '__all__' is not defined

    >>> @public
    ... def some_function():
    ...     pass

    >>> __all__ # noqa: F821
    ['some_function']

    """
    if isinstance(obj, types.FunctionType):
        ns = obj.__globals__
        name = obj.__name__
    elif isinstance(obj, (type(type), type)):
        ns = sys.modules[obj.__module__].__dict__
        name = obj.__name__
    else:
        raise TypeError("expected a function or a class, got %s" % obj)

    if "__all__" not in ns:
        ns["__all__"] = [name]
    else:
        ns["__all__"].append(name)

    return obj

