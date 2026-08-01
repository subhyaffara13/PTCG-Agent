
def get_dialect_registry():
    global _dialect_registry

    if _dialect_registry is None:
        from ._mlir import ir

        _dialect_registry = ir.DialectRegistry()

    return _dialect_registry

