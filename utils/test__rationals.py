
def test_Rationals():
    assert S.Integers.is_subset(S.Rationals)
    assert S.Naturals.is_subset(S.Rationals)
    assert S.Naturals0.is_subset(S.Rationals)
    assert S.Rationals.is_subset(S.Reals)
    assert S.Rationals.inf is -oo
    assert S.Rationals.sup is oo
    it = iter(S.Rationals)
    assert [next(it) for i in range(12)] == [
        0, 1, -1, S.Half, 2, Rational(-1, 2), -2,
        Rational(1, 3), 3, Rational(-1, 3), -3, Rational(2, 3)]
    assert Basic() not in S.Rationals
    assert S.Half in S.Rationals
    assert S.Rationals.contains(0.5) == Contains(
        0.5, S.Rationals, evaluate=False)
    assert 2 in S.Rationals
    r = symbols('r', rational=True)
    assert r in S.Rationals
    raises(TypeError, lambda: x in S.Rationals)
    # issue #18134:
    assert S.Rationals.boundary == S.Reals
    assert S.Rationals.closure == S.Reals
    assert S.Rationals.is_open == False
    assert S.Rationals.is_closed == False


def test_Rationals():
    assert theq(aesara_code_(sy.Integer(2) / 3), true_divide(2, 3))
    assert theq(aesara_code_(S.Half), true_divide(1, 2))


def test_Rationals():
    assert theq(theano_code_(sy.Integer(2) / 3), tt.true_div(2, 3))
    assert theq(theano_code_(S.Half), tt.true_div(1, 2))

