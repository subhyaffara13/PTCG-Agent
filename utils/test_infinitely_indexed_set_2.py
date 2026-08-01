
def test_infinitely_indexed_set_2():
    from sympy.abc import n
    a = Symbol('a', integer=True)
    assert imageset(Lambda(n, n), S.Integers) == \
        imageset(Lambda(n, n + a), S.Integers)
    assert imageset(Lambda(n, n + pi), S.Integers) == \
        imageset(Lambda(n, n + a + pi), S.Integers)
    assert imageset(Lambda(n, n), S.Integers) == \
        imageset(Lambda(n, -n + a), S.Integers)
    assert imageset(Lambda(n, -6*n), S.Integers) == \
        ImageSet(Lambda(n, 6*n), S.Integers)
    assert imageset(Lambda(n, 2*n + pi), S.Integers) == \
        ImageSet(Lambda(n, 2*n + pi - 2), S.Integers)

