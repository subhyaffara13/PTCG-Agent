
def test_failing_powerset__contains__():
    # XXX These are failing when evaluate=True,
    # but using unevaluated PowerSet works fine.
    assert FiniteSet(1, 2) not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Naturals not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Naturals not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)
    assert S.Naturals0 not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Naturals0 not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)
    assert S.Integers not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Integers not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)
    assert S.Rationals not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Rationals not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)
    assert S.Reals not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Reals not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)
    assert S.Complexes not in PowerSet(S.EmptySet).rewrite(FiniteSet)
    assert S.Complexes not in PowerSet(FiniteSet(1, 2)).rewrite(FiniteSet)

