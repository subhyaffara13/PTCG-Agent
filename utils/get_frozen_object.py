
def get_frozen_object(module, paths=None):
    spec = find_spec(module, paths)
    if not spec:
        raise ImportError(f"Can't find {module}")
    return spec.loader.get_code(module)

