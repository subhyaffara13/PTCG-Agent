
def var_builder(prefix: str) -> tuple[VarRanges, Callable[[sympy.Expr], sympy.Symbol]]:
    cnt = itertools.count()
    var_ranges: VarRanges = {}

    def add_var(length: sympy.Expr) -> sympy.Symbol:
        v = sympy_index_symbol(f"{prefix}{next(cnt)}")
        var_ranges[v] = length
        return v

    return var_ranges, add_var

