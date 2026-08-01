
def test_Lambda_symbols():
    assert Lambda(x, 2*x).free_symbols == set()
    assert Lambda(x, x*y).free_symbols == {y}
    assert Lambda((), 42).free_symbols == set()
    assert Lambda((), x*y).free_symbols == {x,y}

