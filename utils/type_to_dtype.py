
def type_to_dtype(typ: type) -> torch.dtype:
    """
    Computes the corresponding dtype for a Number type.
    """

    if not isinstance(typ, type):
        raise AssertionError(f"Expected type, got {type(typ)}")

    if typ in (bool, torch.SymBool):
        return torch.bool
    if typ in (int, torch.SymInt):
        return torch.long
    if typ in (float, torch.SymFloat):
        return torch.get_default_dtype()
    # TODO: sym_complex_float?
    if typ is complex:
        return corresponding_complex_dtype(torch.get_default_dtype())

    raise ValueError(f"Invalid type {typ}!")

