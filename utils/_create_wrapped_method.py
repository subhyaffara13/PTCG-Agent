
def _create_wrapped_method(cls: type, name: str) -> Callable[..., Any]:
    orig_fn = getattr(cls, name)

    @functools.wraps(orig_fn)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        """
        Search the args and kwargs for a Proxy object. If there is one,
        emit a ``call_method`` node to preserve the call to this method
        directly. Otherwise, just return the results of this function
        call, as this function is not being traced.
        """
        proxy = _find_proxy(args, kwargs)
        if proxy is not None:
            return proxy.tracer.create_proxy("call_method", name, args, kwargs)
        return orig_fn(*args, **kwargs)

    return wrapped

