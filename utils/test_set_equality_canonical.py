
def test_set_equality_canonical():
    a, b, c = symbols('a b c')

    A = Eq(FiniteSet(a, b, c), FiniteSet(1, 2, 3))
    B = Ne(FiniteSet(a, b, c), FiniteSet(4, 5, 6))

    assert A.canonical == A.reversed
    assert B.canonical == B.reversed

