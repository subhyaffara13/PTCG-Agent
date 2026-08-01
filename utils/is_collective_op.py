
def is_collective_op(op_name: str) -> bool:
    """Check if an operation is a collective operation."""
    return op_name in COLLECTIVE_OPS

