
def memoize(fun):
    """A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>

    It supports:
     - functions
     - classes (acts as a @singleton)
     - staticmethods
     - classmethods

    It does NOT support:
     - methods
    """

    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            return cache[key]
        except KeyError:
            try:
                ret = cache[key] = fun(*args, **kwargs)
            except Exception as err:
                raise err from None
            return ret

    def cache_clear():
        """Clear cache."""
        cache.clear()

    cache = {}
    wrapper.cache_clear = cache_clear
    return wrapper


def memoize(func, cache=None, key=None):
    """ Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed.
        Only use on pure functions.

    >>> def add(x, y):  return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y

    Use the ``cache`` keyword to provide a dict-like object as an initial cache

    >>> @memoize(cache={(1, 2): 3})
    ... def add(x, y):
    ...     return x + y

    Note that the above works as a decorator because ``memoize`` is curried.

    It is also possible to provide a ``key(args, kwargs)`` function that
    calculates keys used for the cache, which receives an ``args`` tuple and
    ``kwargs`` dict as input, and must return a hashable value.  However,
    the default key function should be sufficient most of the time.

    >>> # Use key function that ignores extraneous keyword arguments
    >>> @memoize(key=lambda args, kwargs: args)
    ... def add(x, y, verbose=False):
    ...     if verbose:
    ...         print('Calculating %s + %s' % (x, y))
    ...     return x + y
    """
    if cache is None:
        cache = {}

    try:
        may_have_kwargs = has_keywords(func) is not False
        # Is unary function (single arg, no variadic argument or keywords)?
        is_unary = is_arity(1, func)
    except TypeError:  # pragma: no cover
        may_have_kwargs = True
        is_unary = False

    if key is None:
        if is_unary:
            def key(args, kwargs):
                return args[0]
        elif may_have_kwargs:
            def key(args, kwargs):
                return (
                    args or None,
                    frozenset(kwargs.items()) if kwargs else None,
                )
        else:
            def key(args, kwargs):
                return args

    def memof(*args, **kwargs):
        k = key(args, kwargs)
        try:
            return cache[k]
        except TypeError:
            raise TypeError("Arguments to memoized function must be hashable")
        except KeyError:
            cache[k] = result = func(*args, **kwargs)
            return result

    try:
        memof.__name__ = func.__name__
    except AttributeError:
        pass
    memof.__doc__ = func.__doc__
    memof.__wrapped__ = func
    return memof


def memoize(rule: Callable[[_S], _T]) -> Callable[[_S], _T]:
    """Memoized version of a rule

    Notes
    =====

    This cache can grow infinitely, so it is not recommended to use this
    than ``functools.lru_cache`` unless you need very heavy computation.
    """
    cache: dict[_S, _T] = {}

    def memoized_rl(expr: _S) -> _T:
        if expr in cache:
            return cache[expr]
        else:
            result = rule(expr)
            cache[expr] = result
            return result
    return memoized_rl


def memoize(func):
    cache = {}

    def wrapped(*args, **kwargs):
        key = (tuple(args), tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapped

