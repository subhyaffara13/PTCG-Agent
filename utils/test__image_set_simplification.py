
def test_ImageSet_simplification():
    from sympy.abc import n, m
    assert imageset(Lambda(n, n), S.Integers) == S.Integers
    assert imageset(Lambda(n, sin(n)),
                    imageset(Lambda(m, tan(m)), S.Integers)) == \
            imageset(Lambda(m, sin(tan(m))), S.Integers)
    assert imageset(n, 1 + 2*n, S.Naturals) == Range(3, oo, 2)
    assert imageset(n, 1 + 2*n, S.Naturals0) == Range(1, oo, 2)
    assert imageset(n, 1 - 2*n, S.Naturals) == Range(-1, -oo, -2)

