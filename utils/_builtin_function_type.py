
def _builtin_function_type(func):
    # a hack to make at least ffi.typeof(builtin_function) work,
    # if the builtin function was obtained by 'vengine_cpy'.
    import sys
    try:
        module = sys.modules[func.__module__]
        ffi = module._cffi_original_ffi
        types_of_builtin_funcs = module._cffi_types_of_builtin_funcs
        tp = types_of_builtin_funcs[func]
    except (KeyError, AttributeError, TypeError):
        return None
    else:
        with ffi._lock:
            return ffi._get_cached_btype(tp)

