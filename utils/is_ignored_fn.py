
def is_ignored_fn(fn) -> bool:
    mod = get_torchscript_modifier(fn)
    return (
        mod is FunctionModifiers.UNUSED
        or mod is FunctionModifiers.IGNORE
        or mod is FunctionModifiers._DROP
    )

