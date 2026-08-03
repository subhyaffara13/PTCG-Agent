import sys

def is_stdlib(mod: object) -> bool:
    if not isinstance(mod, types.ModuleType):
        return False
    return mod.__name__.split(".")[0] in sys.stdlib_module_names

