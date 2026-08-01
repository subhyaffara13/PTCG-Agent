
def test_solveset_real_exp():
    assert solveset(Eq((-2)**x, 4), x, S.Reals) == FiniteSet(2)
    assert solveset(Eq(-2**x, 4), x, S.Reals) == S.EmptySet
    assert solveset(Eq((-3)**x, 27), x, S.Reals) == S.EmptySet
    assert solveset(Eq((-5)**(x+1), 625), x, S.Reals) == FiniteSet(3)
    assert solveset(Eq(2**(x-3), -16), x, S.Reals) == S.EmptySet
    assert solveset(Eq((-3)**(x - 3), -3**39), x, S.Reals) == FiniteSet(42)
    assert solveset(Eq(2**x, y), x, S.Reals) == Intersection(S.Reals, FiniteSet(log(y)/log(2)))

    assert invert_real((-2)**(2*x) - 16, 0, x) == (x, FiniteSet(2))

