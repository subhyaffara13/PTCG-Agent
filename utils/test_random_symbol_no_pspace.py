
def test_random_symbol_no_pspace():
    x = RandomSymbol(Symbol('x'))
    assert x.pspace == PSpace()

