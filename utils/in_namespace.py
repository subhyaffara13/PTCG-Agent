from typing import Any

def in_namespace(
    op: Any | torch._ops.OpOverloadPacket | torch._ops.OpOverload, namespace: str
) -> bool:
    if isinstance(op, torch._ops.OpOverloadPacket):
        return namespace in op._qualified_op_name
    elif isinstance(op, torch._ops.OpOverload):
        return namespace in op.name()
    return False

