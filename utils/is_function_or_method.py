
def is_function_or_method(the_callable):
    # A stricter version of `inspect.isroutine` that does not pass for built-in
    # functions
    return inspect.isfunction(the_callable) or inspect.ismethod(the_callable)

