
def test_minimum():
    assert minimum(sin(x), x) is S.NegativeOne
    assert minimum(sin(x), x, Interval(1, 4)) == sin(4)
    assert minimum(tan(x), x) is -oo
    assert minimum(tan(x), x, Interval(-pi/4, pi/4)) is S.NegativeOne
    assert minimum(sin(x)*cos(x), x, S.Reals) == Rational(-1, 2)
    assert simplify(minimum(sin(x)*cos(x), x, Interval(pi*Rational(3, 8), pi*Rational(5, 8)))
        ) == -sqrt(2)/4
    assert minimum((x+3)*(x-2), x) == Rational(-25, 4)
    assert minimum((x+3)/(x-2), x, Interval(-5, 0)) == Rational(-3, 2)
    assert minimum(x**4-x**3+x**2+10, x) == S(10)
    assert minimum(exp(x), x, Interval(-2, oo)) == exp(-2)
    assert minimum(log(x) - x, x, S.Reals) is -oo
    assert minimum(cos(x), x, Union(Interval(0, 5), Interval(-6, -3))
        ) is S.NegativeOne
    assert minimum(cos(x)-sin(x), x, S.Reals) == -sqrt(2)
    assert minimum(y, x, S.Reals) == y
    assert minimum(x/sqrt(x**2+1), x, S.Reals) == -1

    raises(ValueError, lambda : minimum(sin(x), x, S.EmptySet))
    raises(ValueError, lambda : minimum(log(cos(x)), x, S.EmptySet))
    raises(ValueError, lambda : minimum(1/(x**2 + y**2 + 1), x, S.EmptySet))
    raises(ValueError, lambda : minimum(sin(x), sin(x)))
    raises(ValueError, lambda : minimum(sin(x), x*y, S.EmptySet))
    raises(ValueError, lambda : minimum(sin(x), S.One))


def test_minimum(a_shape, b_shape):
    rng = np.random.default_rng(23409823)
    a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SparseEfficiencyWarning)
        res = a.minimum(b)
        exp = np.minimum(a.toarray(), b.toarray())
        assert_equal(res.toarray(), exp)

