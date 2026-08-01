
def _get_overloads(obj):
    # check for cached compiled fns
    existing_compiled_fns = _try_get_jit_cached_overloads(obj)
    qual_name = _qualified_name(obj)
    uncompiled_overloads = _jit_internal._get_fn_overloads(qual_name)
    if uncompiled_overloads is None:
        return existing_compiled_fns

    if obj in uncompiled_overloads:
        raise RuntimeError(
            _jit_internal.get_overload_no_implementation_error_message("function", obj)
        )

    compiled_fns = [
        _compile_function_with_overload(overload_fn, qual_name, obj)
        for overload_fn in uncompiled_overloads
    ]

    if existing_compiled_fns:
        compiled_fns = existing_compiled_fns + compiled_fns

    # cache compilation, remove information stored to do compilation
    _set_jit_overload_cache(obj, compiled_fns)
    _jit_internal._clear_fn_overloads(qual_name)
    return compiled_fns

