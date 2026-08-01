
def _is_constant_int_like(i):
    return (
        isinstance(i, Value)
        and isinstance(i.owner, arith.ConstantOp)
        and isinstance(i.type, (IntegerType, IndexType))
    )

