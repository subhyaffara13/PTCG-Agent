
def test_powerset__iter__():
    a = PowerSet(FiniteSet(1, 2)).__iter__()
    assert next(a) == S.EmptySet
    assert next(a) == FiniteSet(1)
    assert next(a) == FiniteSet(2)
    assert next(a) == FiniteSet(1, 2)

    a = PowerSet(S.Naturals).__iter__()
    assert next(a) == S.EmptySet
    assert next(a) == FiniteSet(1)
    assert next(a) == FiniteSet(2)
    assert next(a) == FiniteSet(1, 2)
    assert next(a) == FiniteSet(3)
    assert next(a) == FiniteSet(1, 3)
    assert next(a) == FiniteSet(2, 3)
    assert next(a) == FiniteSet(1, 2, 3)

