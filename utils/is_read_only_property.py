
def is_read_only_property(runtime: object) -> bool:
    return isinstance(runtime, property) and runtime.fset is None and runtime.fdel is None

