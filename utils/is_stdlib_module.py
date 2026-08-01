
def is_stdlib_module(modname: str) -> bool:
    """Return: True if the modname is in the standard library"""
    return modname.split(".")[0] in stdlib_module_names


def is_stdlib_module(module: str) -> bool:
    base_module = module.partition(".")[0]
    return base_module in _get_stdlib_modules()

