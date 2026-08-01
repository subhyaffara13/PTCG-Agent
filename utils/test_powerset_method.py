
def test_powerset_method():
    # EmptySet
    A = FiniteSet()
    pset = A.powerset()
    assert len(pset) == 1
    assert pset ==  FiniteSet(S.EmptySet)

    # FiniteSets
    A = FiniteSet(1, 2)
    pset = A.powerset()
    assert len(pset) == 2**len(A)
    assert pset == FiniteSet(FiniteSet(), FiniteSet(1),
                             FiniteSet(2), A)
    # Not finite sets
    A = Interval(0, 1)
    assert A.powerset() == PowerSet(A)

