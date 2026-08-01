
def test_finiteset_simplify():
    S = FiniteSet(1, cos(1)**2 + sin(1)**2)
    assert S.simplify() == {1}

