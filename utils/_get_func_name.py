
def _get_func_name(op: OpType) -> str:
    """Get the name of the implementation function from the op."""
    return f"{_get_op_name(op)}_impl"

