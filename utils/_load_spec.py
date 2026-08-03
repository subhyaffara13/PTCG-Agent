import sys

def _load_spec(spec: ModuleSpec, module_name: str) -> ModuleType:
    name = getattr(spec, "__name__", module_name)
    if name in sys.modules:
        return sys.modules[name]
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # cache (it also ensures `==` works on loaded items)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

