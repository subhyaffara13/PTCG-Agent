
def test_Idx_fixed_bounds():
    i, a, b, x = symbols('i a b x', integer=True)
    assert Idx(x).lower is None
    assert Idx(x).upper is None
    assert Idx(x, a).lower == 0
    assert Idx(x, a).upper == a - 1
    assert Idx(x, 5).lower == 0
    assert Idx(x, 5).upper == 4
    assert Idx(x, oo).lower == 0
    assert Idx(x, oo).upper is oo
    assert Idx(x, (a, b)).lower == a
    assert Idx(x, (a, b)).upper == b
    assert Idx(x, (1, 5)).lower == 1
    assert Idx(x, (1, 5)).upper == 5
    assert Idx(x, (-oo, oo)).lower is -oo
    assert Idx(x, (-oo, oo)).upper is oo

