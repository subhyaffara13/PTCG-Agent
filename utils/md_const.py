
def md_const(val, *, width=32, context=None):
    if not isinstance(val, int):
        raise NotImplementedError(
            f"{val=} not supported; only integers currently supported."
        )
    i_type = IntegerType.get_signless(width, context=context)
    return MDConstantAttr.get(IntegerAttr.get(i_type, val), context=context)

