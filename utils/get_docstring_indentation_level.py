
def get_docstring_indentation_level(func):
    """Return the indentation level of the start of the docstring of a class or function (or method)."""
    # We assume classes are always defined in the global scope
    if inspect.isclass(func):
        return 4
    source = inspect.getsource(func)
    first_line = source.splitlines()[0]
    function_def_level = len(first_line) - len(first_line.lstrip())
    return 4 + function_def_level

