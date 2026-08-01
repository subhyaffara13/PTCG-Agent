
def test_float_handling():
    def test(e1, e2):
        return len(e1.atoms(Float)) == len(e2.atoms(Float))
    assert solve(x - 0.5, rational=True)[0].is_Rational
    assert solve(x - 0.5, rational=False)[0].is_Float
    assert solve(x - S.Half, rational=False)[0].is_Rational
    assert solve(x - 0.5, rational=None)[0].is_Float
    assert solve(x - S.Half, rational=None)[0].is_Rational
    assert test(nfloat(1 + 2*x), 1.0 + 2.0*x)
    for contain in [list, tuple, set]:
        ans = nfloat(contain([1 + 2*x]))
        assert type(ans) is contain and test(list(ans)[0], 1.0 + 2.0*x)
    k, v = list(nfloat({2*x: [1 + 2*x]}).items())[0]
    assert test(k, 2*x) and test(v[0], 1.0 + 2.0*x)
    assert test(nfloat(cos(2*x)), cos(2.0*x))
    assert test(nfloat(3*x**2), 3.0*x**2)
    assert test(nfloat(3*x**2, exponent=True), 3.0*x**2.0)
    assert test(nfloat(exp(2*x)), exp(2.0*x))
    assert test(nfloat(x/3), x/3.0)
    assert test(nfloat(x**4 + 2*x + cos(Rational(1, 3)) + 1),
            x**4 + 2.0*x + 1.94495694631474)
    # don't call nfloat if there is no solution
    tot = 100 + c + z + t
    assert solve(((.7 + c)/tot - .6, (.2 + z)/tot - .3, t/tot - .1)) == []

