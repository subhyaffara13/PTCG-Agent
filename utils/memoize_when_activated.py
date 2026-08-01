
def memoize_when_activated(fun):
    """A memoize decorator which is disabled by default. It can be
    activated and deactivated on request.
    For efficiency reasons it can be used only against class methods
    accepting no arguments.

    >>> class Foo:
    ...     @memoize
    ...     def foo()
    ...         print(1)
    ...
    >>> f = Foo()
    >>> # deactivated (default)
    >>> foo()
    1
    >>> foo()
    1
    >>>
    >>> # activated
    >>> foo.cache_activate(self)
    >>> foo()
    1
    >>> foo()
    >>> foo()
    >>>
    """

    @functools.wraps(fun)
    def wrapper(self):
        try:
            # case 1: we previously entered oneshot() ctx
            ret = self._cache[fun]
        except AttributeError:
            # case 2: we never entered oneshot() ctx
            try:
                return fun(self)
            except Exception as err:
                raise err from None
        except KeyError:
            # case 3: we entered oneshot() ctx but there's no cache
            # for this entry yet
            try:
                ret = fun(self)
            except Exception as err:
                raise err from None
            try:
                self._cache[fun] = ret
            except AttributeError:
                # multi-threading race condition, see:
                # https://github.com/giampaolo/psutil/issues/1948
                pass
        return ret

    def cache_activate(proc):
        """Activate cache. Expects a Process instance. Cache will be
        stored as a "_cache" instance attribute.
        """
        proc._cache = {}

    def cache_deactivate(proc):
        """Deactivate and clear cache."""
        try:
            del proc._cache
        except AttributeError:
            pass

    wrapper.cache_activate = cache_activate
    wrapper.cache_deactivate = cache_deactivate
    return wrapper

