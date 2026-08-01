
def _prepare_async_lookup_callable(request):
    """Unwraps a request callable, clones the transport, and returns the new callable.

    Args:
        request: The original request callable (e.g. functools.partial or raw Request).

    Returns:
        Tuple[Callable, Any, bool]: A tuple containing the new lookup callable, the
            underlying request object, and a boolean indicating if it was cloned.
    """
    is_partial = isinstance(request, functools.partial)
    base_callable = request.func if is_partial else request

    if not hasattr(base_callable, "_clone"):
        return request, base_callable, False

    cloned_callable = base_callable._clone()
    is_cloned = cloned_callable is not base_callable

    if is_partial:
        new_request = functools.partial(
            cloned_callable, *request.args, **request.keywords
        )
    else:
        new_request = cloned_callable

    return new_request, cloned_callable, is_cloned

