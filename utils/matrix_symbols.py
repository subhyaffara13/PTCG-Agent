
def matrix_symbols(expr):
    return [sym for sym in expr.free_symbols if sym.is_Matrix]

