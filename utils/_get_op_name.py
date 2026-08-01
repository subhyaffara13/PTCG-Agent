
def _get_op_name(op: OpType) -> str:
    """Get the op name from the op."""
    if isinstance(op, OpOverload):
        op = op.overloadpacket
    return str(op).split(".", 1)[1]


def _get_op_name(op) -> str:
    if isinstance(op, torch._ops.OpOverload):
        op_name = op.__qualname__
    elif hasattr(op, "__module__") and hasattr(op, "__name__"):
        op_name = f"{op.__module__}.{op.__name__}"
    else:
        op_name = str(op)
    return op_name

