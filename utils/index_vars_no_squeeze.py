
def index_vars_no_squeeze(
    *argsizes: Sequence[sympy.Expr], prefix: str
) -> tuple[list[list[sympy.Symbol]], VarRanges]:
    var_ranges, add_var = var_builder(prefix)
    args: list[list[sympy.Symbol]] = [list(map(add_var, size)) for size in argsizes]
    return args, var_ranges

