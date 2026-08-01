
def inductor_compiled_code_impl(func, inputs, *, name=None):
    resolved = _resolve_inductor_callable(func)
    return resolved.compiled_callable(inputs)

