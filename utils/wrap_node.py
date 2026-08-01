
def wrap_node(x: SymNode) -> SymInt | SymFloat | SymBool | int | float | bool:
    # TODO: let C++ also take advantage of this
    if isinstance(x, SymNode) and x.constant is not None:
        return x.constant
    if x.is_int():
        return SymInt(x)
    elif x.is_float():
        return SymFloat(x)
    elif x.is_bool():
        return SymBool(x)
    else:
        raise AssertionError(f"unrecognized return type {x}")

