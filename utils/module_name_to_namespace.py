
def module_name_to_namespace(name: str) -> ModuleType:
    return module_namespace(importlib.import_module(name))

