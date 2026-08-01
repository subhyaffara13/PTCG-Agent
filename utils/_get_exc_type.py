
def _get_exc_type(cls: Type[Exception]) -> str:
    if issubclass(cls, AssertionError):
        return 'assertion_error'

    base_name = 'type_error' if issubclass(cls, TypeError) else 'value_error'
    if cls in (TypeError, ValueError):
        # just TypeError or ValueError, no extra code
        return base_name

    # if it's not a TypeError or ValueError, we just take the lowercase of the exception name
    # no chaining or snake case logic, use "code" for more complex error types.
    code = getattr(cls, 'code', None) or cls.__name__.replace('Error', '').lower()
    return base_name + '.' + code

