
def ignore_builtins(op: torch._ops.OpOverload) -> bool:
    return op.namespace in ("aten", "prims", "prim")

