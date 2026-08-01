
def _is_drop_fn(fn) -> bool:
    mod = get_torchscript_modifier(fn)
    return mod is FunctionModifiers._DROP

