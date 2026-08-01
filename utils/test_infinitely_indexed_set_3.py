
def test_infinitely_indexed_set_3():
    from sympy.abc import n, m
    assert imageset(Lambda(m, 2*pi*m), S.Integers).intersect(
            imageset(Lambda(n, 3*pi*n), S.Integers)).dummy_eq(
        ImageSet(Lambda(t, 6*pi*t), S.Integers))
    assert imageset(Lambda(n, 2*n + 1), S.Integers) == \
        imageset(Lambda(n, 2*n - 1), S.Integers)
    assert imageset(Lambda(n, 3*n + 2), S.Integers) == \
        imageset(Lambda(n, 3*n - 1), S.Integers)

