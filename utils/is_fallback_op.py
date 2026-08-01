
def is_fallback_op(
    node: Operation | None,
    op: torch._ops.OpOverload | Collection[torch._ops.OpOverload],
) -> bool:
    from . import ir

    if isinstance(op, torch._ops.OpOverload):
        op = [op]
    return isinstance(node, ir.FallbackKernel) and node.op_overload in op

