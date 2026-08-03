import sys

def import_fresh_module(name: str, blocked: list[str]) -> ModuleType:
    # Keep track of modules saved for later restoration as well
    # as those which just need a blocking entry removed
    names = {name, *blocked}
    orig_modules = _save_and_remove_modules(names)
    for modname in blocked:
        sys.modules[modname] = None  # type: ignore[assignment]

    try:
        return importlib.import_module(name)
    finally:
        _save_and_remove_modules(names)
        sys.modules.update(orig_modules)

