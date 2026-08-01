
def index_vars_squeeze(
    *argsizes: Sequence[sympy.Expr], prefix: str = "d"
) -> tuple[list[Sequence[sympy.Expr]], VarRanges]:
    from .ir import SqueezeView

    var_ranges, add_var = var_builder(prefix)
    args: list[Sequence[sympy.Expr]] = []
    new_sizes: list[Sequence[sympy.Expr]] = []
    for size in argsizes:
        new_size, reindex = SqueezeView.squeezer(size)
        new_sizes.append(new_size)
        args.append(reindex(list(map(add_var, new_size))))
    return args, var_ranges

