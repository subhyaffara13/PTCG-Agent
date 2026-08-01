
def _reset_eom_method(method):
    """Decorator to reset the eom_method if a property is changed."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._eom_method = None
        return method(self, *args, **kwargs)

    return wrapper

