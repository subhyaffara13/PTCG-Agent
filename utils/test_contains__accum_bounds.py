
def test_contains_AccumBounds():
    assert (1 in B(1, 2)) == S.true
    raises(TypeError, lambda: a in B(1, 2))
    assert 0 in B(-1, 0)
    raises(TypeError, lambda:
        (cos(1)**2 + sin(1)**2 - 1) in B(-1, 0))
    assert (-oo in B(1, oo)) == S.true
    assert (oo in B(-oo, 0)) == S.true

    # issue 13159
    assert Mul(0, B(-1, 1)) == Mul(B(-1, 1), 0) == 0
    import itertools
    for perm in itertools.permutations([0, B(-1, 1), x]):
        assert Mul(*perm) == 0

