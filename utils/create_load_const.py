
def create_load_const(val: Any, checked: bool = True) -> Instruction:
    """
    In general we should only create `LOAD_CONST` for immutable objects, but
    sometimes it's convenient _and safe_ for Dynamo create `LOAD_CONST` for
    mutable objects. In such cases, use `checked=False`.
    """
    if checked:
        assert is_safe_constant(val), f"unsafe constant {val}"
    return create_instruction("LOAD_CONST", argval=val)

