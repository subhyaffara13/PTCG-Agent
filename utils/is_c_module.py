import os

def is_c_module(module: ModuleType) -> bool:
    if module.__dict__.get("__file__") is None:
        # Could be a namespace package. These must be handled through
        # introspection, since there is no source file.
        return True
    return os.path.splitext(module.__dict__["__file__"])[-1] in [".so", ".pyd", ".dll"]

