
def num_bitmap_args(args: tuple[RuntimeArg, ...]) -> int:
    n = 0
    for arg in args:
        if arg.type.error_overlap and arg.kind.is_optional():
            n += 1
    return (n + (BITMAP_BITS - 1)) // BITMAP_BITS


def num_bitmap_args(builder: IRBuilder, args: list[Argument]) -> int:
    n = 0
    for arg in args:
        t = builder.type_to_rtype(arg.variable.type)
        if t.error_overlap and arg.kind.is_optional():
            n += 1
    return (n + (BITMAP_BITS - 1)) // BITMAP_BITS

