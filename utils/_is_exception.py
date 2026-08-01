
def _is_exception(obj) -> bool:
    if not inspect.isclass(obj):
        return False
    return issubclass(obj, Exception)

