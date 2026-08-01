
def _check_directly_compile_overloaded(obj):
    qual_name = _qualified_name(obj)
    if _jit_internal._get_fn_overloads(qual_name) or _try_get_jit_cached_overloads(obj):
        raise RuntimeError(
            f"Function {qual_name} cannot be directly compiled because it"
            " is overloaded. It must be used in a context of a function"
            " where its inputs can determine which overload to call."
        )

