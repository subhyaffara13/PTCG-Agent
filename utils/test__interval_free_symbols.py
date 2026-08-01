
def test_Interval_free_symbols():
    # issue 6211
    assert Interval(0, 1).free_symbols == set()
    x = Symbol('x', real=True)
    assert Interval(0, x).free_symbols == {x}

