
def _method_from_src(
    method_name: str, src: str, globals: dict[str, Any], co_fields=None
) -> Callable:
    # avoid mutating the passed in dict
    globals_copy = globals.copy()
    _exec_with_source(src, globals_copy, co_fields)
    fn = globals_copy[method_name]
    del globals_copy[method_name]
    return fn

