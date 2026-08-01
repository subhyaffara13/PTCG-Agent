
def _create_wrapped_func(orig_fn: Callable[_P, _T]) -> Callable[_P, _T]:
    @functools.wraps(orig_fn)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> Any:
        """
        Given an closed-over ``orig_function`` to invoke, search the args and kwargs for
        a Proxy object. If there is one, emit a ``call_function`` node to preserve the
        call to this leaf function directly. Otherwise, just return the results of
        this function call, as this function is not being traced.
        """
        proxy = _find_proxy(args, kwargs)
        if proxy is not None:
            return_proxy = proxy.tracer.create_proxy(
                "call_function", orig_fn, args, kwargs
            )
            return_proxy.node.meta["is_wrapped"] = True
            return return_proxy
        return orig_fn(*args, **kwargs)

    return wrapped

