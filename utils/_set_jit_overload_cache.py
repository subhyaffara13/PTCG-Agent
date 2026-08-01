
def _set_jit_overload_cache(key, compiled_fns) -> None:
    _jit_function_overload_caching[key] = [fn.qualified_name for fn in compiled_fns]

