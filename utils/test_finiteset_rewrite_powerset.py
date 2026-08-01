
def test_finiteset_rewrite_powerset():
    assert FiniteSet(S.EmptySet).rewrite(PowerSet) == PowerSet(S.EmptySet)
    assert FiniteSet(
        S.EmptySet, FiniteSet(1),
        FiniteSet(2), FiniteSet(1, 2)).rewrite(PowerSet) == \
            PowerSet(FiniteSet(1, 2))
    assert FiniteSet(1, 2, 3).rewrite(PowerSet) == FiniteSet(1, 2, 3)

