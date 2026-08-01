
def _is_inplace_op(op: OpOverload | Callable[..., Any]) -> bool:
    return (
        isinstance(op, OpOverload)
        # Not precise heuristic to detect inplace operation
        and op._schema.name[-1] == "_"
        # Strengthen the heuristic to check that the first argument and return value are a write
        and len(op._schema.arguments) > 0
        and op._schema.arguments[0].is_write
        and len(op._schema.returns) > 0
        and op._schema.returns[0].is_write
    )

