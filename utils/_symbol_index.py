
def _symbol_index(sym: sympy.Symbol, sym_type: SymT):
    return int(str(sym)[len(prefix_str[sym_type]) :])

