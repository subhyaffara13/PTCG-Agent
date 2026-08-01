
def test_powerset_creation():
    assert unchanged(PowerSet, FiniteSet(1, 2))
    assert unchanged(PowerSet, S.EmptySet)
    raises(ValueError, lambda: PowerSet(123))
    assert unchanged(PowerSet, S.Reals)
    assert unchanged(PowerSet, S.Integers)

