
def test_symbols_exhausted_error():
    l = cos(x+y)+x+y+cos(w+y)+sin(w+y)
    sym = [x, y, z]
    with raises(ValueError):
        cse(l, symbols=sym)

