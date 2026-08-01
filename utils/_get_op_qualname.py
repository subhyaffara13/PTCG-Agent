
def _get_op_qualname(op: _op_identifier) -> str:
    """Convert an op identifier to a qualified string key."""
    if isinstance(op, torch._ops.OpOverload):
        return op._name
    elif isinstance(op, torch._ops.HigherOrderOperator):
        return f"{op.namespace}::{op.name()}"
    elif isinstance(op, CustomOpDef):
        return op._qualname
    elif isinstance(op, str):
        return op

    raise ValueError(f"Invalid operator input {op}")

