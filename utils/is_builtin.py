
def is_builtin(op: OpOverload) -> bool:
    if not isinstance(op, OpOverload):
        raise AssertionError(f"op must be OpOverload, got {type(op)}")
    return op.namespace in {"aten", "prim", "prims"}


def is_builtin(op: OpOverload) -> bool:
    return op.namespace in _is_builtin_namespaces


def is_builtin(op):
    return op.namespace in ('aten', 'prims', 'prim')


def is_builtin(name: str) -> bool:
    """Return true if <name> could be considered as a builtin defined by python."""
    return name in builtins or name in SPECIAL_BUILTINS  # type: ignore[operator]

