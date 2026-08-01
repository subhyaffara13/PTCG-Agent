
def autocast_decorator(autocast_instance, func):
    @functools.wraps(func)
    def decorate_autocast(*args, **kwargs):
        with autocast_instance:
            return func(*args, **kwargs)

    decorate_autocast.__script_unsupported = (  # type: ignore[attr-defined]
        "@autocast() decorator is not supported in script mode"
    )
    return decorate_autocast

