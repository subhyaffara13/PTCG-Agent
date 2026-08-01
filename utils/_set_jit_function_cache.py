
def _set_jit_function_cache(key, value) -> None:
    # only free functions currently supported
    if not isinstance(value, torch.jit.ScriptFunction):
        raise AssertionError(f"Expected ScriptFunction, got {type(value)}")
    _jit_caching_layer[key] = value.qualified_name

