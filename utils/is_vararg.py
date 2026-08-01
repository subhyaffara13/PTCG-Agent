
def is_vararg(the_callable):
    if not is_function_or_method(the_callable) and callable(the_callable):  # noqa: B004
        # If `the_callable` is a class, de-sugar the call so we can still get
        # the signature
        the_callable = the_callable.__call__

    if is_function_or_method(the_callable):
        return inspect.getfullargspec(the_callable).varargs is not None
    else:
        return False

