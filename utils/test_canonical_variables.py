
def test_canonical_variables():
    x, i0, i1 = symbols('x _:2')
    assert Integral(x, (x, x + 1)).canonical_variables == {x: i0}
    assert Integral(x, (x, x + 1), (i0, 1, 2)).canonical_variables == {
        x: i0, i0: i1}
    assert Integral(x, (x, x + i0)).canonical_variables == {x: i1}

