
def test_transolve():

    assert _transolve(3**x, x, S.Reals) == S.EmptySet
    assert _transolve(3**x - 9**(x + 5), x, S.Reals) == FiniteSet(-10)

