
def _extract_code_globals(co):
    """Find all globals names read or written to by codeblock co."""
    out_names = _extract_code_globals_cache.get(co)
    if out_names is None:
        # We use a dict with None values instead of a set to get a
        # deterministic order and avoid introducing non-deterministic pickle
        # bytes as a results.
        out_names = {name: None for name in _walk_global_ops(co)}

        # Declaring a function inside another one using the "def ..." syntax
        # generates a constant code object corresponding to the one of the
        # nested function's As the nested function may itself need global
        # variables, we need to introspect its code, extract its globals, (look
        # for code object in it's co_consts attribute..) and add the result to
        # code_globals
        if co.co_consts:
            for const in co.co_consts:
                if isinstance(const, types.CodeType):
                    out_names.update(_extract_code_globals(const))

        _extract_code_globals_cache[co] = out_names

    return out_names

