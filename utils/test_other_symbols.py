
def test_other_symbols():
    from sympy.printing.latex import other_symbols
    for s in other_symbols:
        assert latex(symbols(s)) == r"" "\\" + s

