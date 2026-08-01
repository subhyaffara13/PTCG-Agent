
def is_pointer_arithmetic(op: IntOp) -> bool:
    """Check if op is add/subtract targeting pointer_rprimitive and integer of the same size."""
    if op.op not in (IntOp.ADD, IntOp.SUB):
        return False
    if not is_pointer_rprimitive(op.type):
        return False
    left = op.lhs.type
    right = op.rhs.type
    if is_pointer_rprimitive(left):
        return is_valid_ptr_displacement_type(right)
    if is_pointer_rprimitive(right):
        return is_valid_ptr_displacement_type(left)
    return False

