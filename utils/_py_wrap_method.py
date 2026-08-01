
def _py_wrap_method(orig: Callable, __torch_function__: Callable) -> Callable:
    def impl(*args: Any, **kwargs: Any) -> Any:
        return __torch_function__(orig, None, args, kwargs)

    # Copy metadata using functools.update_wrapper for just __name__ and __doc__
    functools.update_wrapper(impl, orig, assigned=("__name__", "__doc__"), updated=())

    return impl

