
def make_symbol(prefix: SymT, idx: int, **kwargs) -> sympy.Symbol:
    # TODO: maybe put the assumptions here directly
    return sympy.Symbol(f"{prefix_str[prefix]}{idx}", **kwargs)

