
def should_drop(fn) -> bool:
    attr = get_torchscript_modifier(fn)
    if attr is None:
        return False
    return attr is FunctionModifiers.UNUSED or attr is FunctionModifiers._DROP

