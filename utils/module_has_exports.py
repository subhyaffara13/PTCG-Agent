
def module_has_exports(mod):
    for name in dir(mod):
        if hasattr(mod, name):
            item = getattr(mod, name)
            if callable(item):
                if get_torchscript_modifier(item) is FunctionModifiers.EXPORT:
                    return True
    return False

