import sys

def _import_module(name):
    """Import module, returning the module after the last dot."""
    __import__(name)
    return sys.modules[name]


def _import_module(import_name, safe=False):
    try:
        if import_name.startswith('__runtime__.'):
            return sys.modules[import_name]
        elif '.' in import_name:
            items = import_name.split('.')
            module = '.'.join(items[:-1])
            obj = items[-1]
            submodule = getattr(__import__(module, None, None, [obj]), obj)
            if isinstance(submodule, (ModuleType, type)):
                return submodule
            return __import__(import_name, None, None, [obj])
        else:
            return __import__(import_name)
    except (ImportError, AttributeError, KeyError):
        if safe:
            return None
        raise


def _import_module(name, path):
    import importlib.util
    from importlib.abc import Loader

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise AssertionError(f"failed to load spec from {path}")
    module = importlib.util.module_from_spec(spec)
    if not isinstance(spec.loader, Loader):
        raise AssertionError(f"expected Loader, got {type(spec.loader)}")
    spec.loader.exec_module(module)
    return module


def _import_module(name: str) -> types.ModuleType:
    """
    Import the named module and cache the result. importlib.import_module()
    seems to do some filesystem checking to validate the name so not caching
    this can be slow.
    """
    return importlib.import_module(name)

