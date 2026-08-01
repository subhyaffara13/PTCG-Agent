
def _get_torchscript_builtins():
    functions = []
    builtins = filter(lambda fn: not _is_math_fn(fn[0]), _get_builtins_helper())
    builtins_list = list(builtins)
    # Iterate over the specially added builtins
    for fn, _builtin_name in builtins_list:
        mod = inspect.getmodule(fn)
        if not mod:
            raise RuntimeError(f"Module for {fn} not found")
        builtin = _find_builtin(fn)
        if builtin is not None:
            schemas = torch._C._jit_get_schemas_for_operator(builtin)
            for schema in schemas:
                functions.append(_emit_schema(mod.__name__, fn.__name__, schema))

    return "TorchScript Builtin Functions", functions

