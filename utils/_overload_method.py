import sys

def _overload_method(func):
    try:
        _check_overload_body(func)
    except IndentationError:
        # CPython 3.13.8 has a bug (https://github.com/python/cpython/issues/139783)
        # where inspect.getsourcelines() returns truncated source when a decorator
        # is followed by a comment, causing ast.parse() to fail with IndentationError.
        # Fixed in 3.13.9. Swallow the error on affected versions; re-raise otherwise.
        if sys.version_info[:3] == (3, 13, 8):
            import warnings

            warnings.warn(
                "Skipping overload body check due to a known CPython 3.13.8 bug "
                "(https://github.com/python/cpython/issues/139783). "
                "Consider upgrading to Python 3.13.9+.",
                stacklevel=2,
            )
        else:
            raise
    qual_name = _qualified_name(func)
    global _overloaded_methods
    class_name_map = _overloaded_methods.get(qual_name)
    if class_name_map is None:
        class_name_map = {}
        _overloaded_methods[qual_name] = class_name_map

    class_name, line_no = get_class_name_lineno(func)
    method_overloads = class_name_map.get(class_name)
    if method_overloads is None:
        method_overloads = []
        class_name_map[class_name] = method_overloads
        _overloaded_method_class_fileno[(qual_name, class_name)] = line_no
    else:
        existing_lineno = _overloaded_method_class_fileno[(qual_name, class_name)]
        if existing_lineno != line_no:
            raise RuntimeError(
                "Cannot currently overload the same method name in two different"
                " classes with the same name in the same module"
            )

    method_overloads.append(func)
    return func

