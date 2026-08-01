
def get_torchscript_modifier(fn):
    if not callable(fn):
        return None
    if hasattr(fn, "__func__"):
        fn = fn.__func__
    return getattr(fn, "_torchscript_modifier", FunctionModifiers.DEFAULT)

