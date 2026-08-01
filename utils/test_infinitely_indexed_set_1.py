
def test_infinitely_indexed_set_1():
    from sympy.abc import n, m
    assert imageset(Lambda(n, n), S.Integers) == imageset(Lambda(m, m), S.Integers)

    assert imageset(Lambda(n, 2*n), S.Integers).intersect(
            imageset(Lambda(m, 2*m + 1), S.Integers)) is S.EmptySet

    assert imageset(Lambda(n, 2*n), S.Integers).intersect(
            imageset(Lambda(n, 2*n + 1), S.Integers)) is S.EmptySet

    assert imageset(Lambda(m, 2*m), S.Integers).intersect(
                imageset(Lambda(n, 3*n), S.Integers)).dummy_eq(
            ImageSet(Lambda(t, 6*t), S.Integers))

    assert imageset(x, x/2 + Rational(1, 3), S.Integers).intersect(S.Integers) is S.EmptySet
    assert imageset(x, x/2 + S.Half, S.Integers).intersect(S.Integers) is S.Integers

    # https://github.com/sympy/sympy/issues/17355
    S53 = ImageSet(Lambda(n, 5*n + 3), S.Integers)
    assert S53.intersect(S.Integers) == S53

