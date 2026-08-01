
def find_module(module, paths=None):
    """Just like 'imp.find_module()', but with package support"""
    spec = find_spec(module, paths)
    if spec is None:
        raise ImportError(f"Can't find {module}")
    if not spec.has_location and hasattr(spec, 'submodule_search_locations'):
        spec = importlib.util.spec_from_loader('__init__.py', spec.loader)

    kind = -1
    file = None
    static = isinstance(spec.loader, type)
    if (
        spec.origin == 'frozen'
        or static
        and issubclass(spec.loader, importlib.machinery.FrozenImporter)
    ):
        kind = PY_FROZEN
        path = None  # imp compabilty
        suffix = mode = ''  # imp compatibility
    elif (
        spec.origin == 'built-in'
        or static
        and issubclass(spec.loader, importlib.machinery.BuiltinImporter)
    ):
        kind = C_BUILTIN
        path = None  # imp compabilty
        suffix = mode = ''  # imp compatibility
    elif spec.has_location:
        path = spec.origin
        suffix = os.path.splitext(path)[1]
        mode = 'r' if suffix in importlib.machinery.SOURCE_SUFFIXES else 'rb'

        if suffix in importlib.machinery.SOURCE_SUFFIXES:
            kind = PY_SOURCE
            file = tokenize.open(path)
        elif suffix in importlib.machinery.BYTECODE_SUFFIXES:
            kind = PY_COMPILED
            file = open(path, 'rb')
        elif suffix in importlib.machinery.EXTENSION_SUFFIXES:
            kind = C_EXTENSION

    else:
        path = None
        suffix = mode = ''

    return file, path, (suffix, mode, kind)

