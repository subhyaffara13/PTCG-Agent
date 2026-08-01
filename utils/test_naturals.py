
def test_naturals():
    N = S.Naturals
    assert 5 in N
    assert -5 not in N
    assert 5.5 not in N
    ni = iter(N)
    a, b, c, d = next(ni), next(ni), next(ni), next(ni)
    assert (a, b, c, d) == (1, 2, 3, 4)
    assert isinstance(a, Basic)

    assert N.intersect(Interval(-5, 5)) == Range(1, 6)
    assert N.intersect(Interval(-5, 5, True, True)) == Range(1, 5)

    assert N.boundary == N
    assert N.is_open == False
    assert N.is_closed == True

    assert N.inf == 1
    assert N.sup is oo
    assert not N.contains(oo)
    for s in (S.Naturals0, S.Naturals):
        assert s.intersection(S.Reals) is s
        assert s.is_subset(S.Reals)

    assert N.as_relational(x) == And(Eq(floor(x), x), x >= 1, x < oo)

