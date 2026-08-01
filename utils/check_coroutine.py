
def check_coroutine(value) -> bool:
    get_coroutine_checker = getattr(sys.modules[__name__], "get_coroutine_checker")
    return get_coroutine_checker().is_async_callable(value)

