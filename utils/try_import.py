
def try_import(module_name: str) -> ModuleType | None:
    # Implementation based on
    # https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported
    if (module := sys.modules.get(module_name, None)) is not None:
        return module

    if (spec := importlib.util.find_spec(module_name)) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        # https://docs.python.org/3/library/importlib.html#importlib.machinery.ModuleSpec.loader
        # "The finder should always set this attribute"
        if spec.loader is None:
            raise AssertionError("The loader attribute should always be set")
        spec.loader.exec_module(module)
        return module

    return None

