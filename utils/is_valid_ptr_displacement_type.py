
def is_valid_ptr_displacement_type(rtype: RType) -> bool:
    """Check if rtype is a valid displacement type for pointer arithmetic."""
    if not (is_fixed_width_rtype(rtype) or is_c_py_ssize_t_rprimitive(rtype)):
        return False
    assert isinstance(rtype, RPrimitive)
    return rtype.size == pointer_rprimitive.size

