
def returns_type(rs: Sequence[Return], *, symint: bool = False) -> CType:
    if len(rs) == 0:
        return BaseCType(voidT)
    elif len(rs) == 1:
        return return_type(rs[0], symint=symint)
    else:
        return TupleCType([return_type(r, symint=symint) for r in rs])


def returns_type(rs: Sequence[Return], *, symint: bool = True) -> CType:
    # At present, there is no difference. But there could be!
    return cpp.returns_type(rs, symint=symint)


def returns_type(func: FunctionSchema) -> CType:
    # Assertion: all view ops return tensor-like outputs
    if len(func.returns) < 1:
        raise AssertionError("Expected at least one return value")
    for ret in func.returns:
        if not ret.type.is_tensor_like():
            raise AssertionError(f"Expected tensor-like return type, got {ret.type}")
    # However, the return type of the lambda is always an individual tensor.
    # For multi-tensor outputs, each tensor needs to be tracked individually.
    return BaseCType(tensorT)


def returns_type(rs: Sequence[Return], *, symint: bool) -> CType:
    return cpp.returns_type(rs, symint=symint)

