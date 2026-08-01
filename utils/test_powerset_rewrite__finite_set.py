
def test_powerset_rewrite_FiniteSet():
    assert PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet) == \
        FiniteSet(S.EmptySet, FiniteSet(1), FiniteSet(2), FiniteSet(1, 2))
    assert PowerSet(S.EmptySet).rewrite(FiniteSet) == FiniteSet(S.EmptySet)
    assert PowerSet(S.Naturals).rewrite(FiniteSet) == PowerSet(S.Naturals)

