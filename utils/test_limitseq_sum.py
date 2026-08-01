
def test_limitseq_sum():
    from sympy.abc import x, y, z
    assert limit_seq(Sum(1/x, (x, 1, y)) - log(y), y) == S.EulerGamma
    assert limit_seq(Sum(1/x, (x, 1, y)) - 1/y, y) is S.Infinity
    assert (limit_seq(binomial(2*x, x) / Sum(binomial(2*y, y), (y, 1, x)), x) ==
            S(3) / 4)
    assert (limit_seq(Sum(y**2 * Sum(2**z/z, (z, 1, y)), (y, 1, x)) /
                  (2**x*x), x) == 4)

