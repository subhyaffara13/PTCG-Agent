from typing import Union

def test_maximum():
    assert maximum(sin(x), x) is S.One
    assert maximum(sin(x), x, Interval(0, 1)) == sin(1)
    assert maximum(tan(x), x) is oo
    assert maximum(tan(x), x, Interval(-pi/4, pi/4)) is S.One
    assert maximum(sin(x)*cos(x), x, S.Reals) == S.Half
    assert simplify(maximum(sin(x)*cos(x), x, Interval(pi*Rational(3, 8), pi*Rational(5, 8)))
        ) == sqrt(2)/4
    assert maximum((x+3)*(x-2), x) is oo
    assert maximum((x+3)*(x-2), x, Interval(-5, 0)) == S(14)
    assert maximum((x+3)/(x-2), x, Interval(-5, 0)) == Rational(2, 7)
    assert simplify(maximum(-x**4-x**3+x**2+10, x)
        ) == 41*sqrt(41)/512 + Rational(5419, 512)
    assert maximum(exp(x), x, Interval(-oo, 2)) == exp(2)
    assert maximum(log(x) - x, x, S.Reals) is S.NegativeOne
    assert maximum(cos(x), x, Union(Interval(0, 5), Interval(-6, -3))
        ) is S.One
    assert maximum(cos(x)-sin(x), x, S.Reals) == sqrt(2)
    assert maximum(y, x, S.Reals) == y
    assert maximum(abs(a**3 + a), a, Interval(0, 2)) == 10
    assert maximum(abs(60*a**3 + 24*a), a, Interval(0, 2)) == 528
    assert maximum(abs(12*a*(5*a**2 + 2)), a, Interval(0, 2)) == 528
    assert maximum(x/sqrt(x**2+1), x, S.Reals) == 1

    raises(ValueError, lambda : maximum(sin(x), x, S.EmptySet))
    raises(ValueError, lambda : maximum(log(cos(x)), x, S.EmptySet))
    raises(ValueError, lambda : maximum(1/(x**2 + y**2 + 1), x, S.EmptySet))
    raises(ValueError, lambda : maximum(sin(x), sin(x)))
    raises(ValueError, lambda : maximum(sin(x), x*y, S.EmptySet))
    raises(ValueError, lambda : maximum(sin(x), S.One))


def test_maximum(a_shape, b_shape):
    rng = np.random.default_rng(23409823)
    a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SparseEfficiencyWarning)
        res = a.maximum(b)
        exp = np.maximum(a.toarray(), b.toarray())
        assert_equal(res.toarray(), exp)

