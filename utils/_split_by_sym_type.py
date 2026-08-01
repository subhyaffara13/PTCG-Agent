
def _split_by_sym_type(
    args: list[Any],
) -> tuple[list[ShapeAsConstantBuffer], list[Any]]:
    non_sym_args = []
    sym_args = []
    for arg in args:
        if isinstance(arg, ShapeAsConstantBuffer):
            sym_args.append(arg.expr)
        else:
            non_sym_args.append(arg)

    return sym_args, non_sym_args

