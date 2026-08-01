
def test_mod():
    if not np:
        skip("NumPy not installed")

    e = Mod(a, b)
    f = lambdify((a, b), e)

    a_ = np.array([0, 1, 2, 3])
    b_ = 2
    assert np.array_equal(f(a_, b_), [0, 1, 0, 1])

    a_ = np.array([0, 1, 2, 3])
    b_ = np.array([2, 2, 2, 2])
    assert np.array_equal(f(a_, b_), [0, 1, 0, 1])

    a_ = np.array([2, 3, 4, 5])
    b_ = np.array([2, 3, 4, 5])
    assert np.array_equal(f(a_, b_), [0, 0, 0, 0])


def test_mod():
    x = S.Half
    y = Rational(3, 4)
    z = Rational(5, 18043)

    assert x % x == 0
    assert x % y == S.Half
    assert x % z == Rational(3, 36086)
    assert y % x == Rational(1, 4)
    assert y % y == 0
    assert y % z == Rational(9, 72172)
    assert z % x == Rational(5, 18043)
    assert z % y == Rational(5, 18043)
    assert z % z == 0

    a = Float(2.6)

    assert (a % .2) == 0.0
    assert (a % 2).round(15) == 0.6
    assert (a % 0.5).round(15) == 0.1

    p = Symbol('p', infinite=True)

    assert oo % oo is nan
    assert zoo % oo is nan
    assert 5 % oo is nan
    assert p % 5 is nan

    # In these two tests, if the precision of m does
    # not match the precision of the ans, then it is
    # likely that the change made now gives an answer
    # with degraded accuracy.
    r = Rational(500, 41)
    f = Float('.36', 3)
    m = r % f
    ans = Float(r % Rational(f), 3)
    assert m == ans and m._prec == ans._prec
    f = Float('8.36', 3)
    m = f % r
    ans = Float(Rational(f) % r, 3)
    assert m == ans and m._prec == ans._prec

    s = S.Zero

    assert s % float(1) == 0.0

    # No rounding required since these numbers can be represented
    # exactly.
    assert Rational(3, 4) % Float(1.1) == 0.75
    assert Float(1.5) % Rational(5, 4) == 0.25
    assert Rational(5, 4).__rmod__(Float('1.5')) == 0.25
    assert Float('1.5').__rmod__(Float('2.75')) == Float('1.25')
    assert 2.75 % Float('1.5') == Float('1.25')

    a = Integer(7)
    b = Integer(4)

    assert type(a % b) == Integer
    assert a % b == Integer(3)
    assert Integer(1) % Rational(2, 3) == Rational(1, 3)
    assert Rational(7, 5) % Integer(1) == Rational(2, 5)
    assert Integer(2) % 1.5 == 0.5

    assert Integer(3).__rmod__(Integer(10)) == Integer(1)
    assert Integer(10) % 4 == Integer(2)
    assert 15 % Integer(4) == Integer(3)


def test_mod():
    assert h%l == h%x == 1
    assert l%h == x%h == 2
    assert x%l == Mod(x, -1)
    assert l%x == Mod(-1, x)


def test_mod(dtype):
    a = pd.array([1, 2, 3, None, 5], dtype=dtype)
    b = pd.array([0, 1, None, 3, 4], dtype=dtype)

    result = a % b
    expected = pd.array([0, 0, None, None, 1], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)


def test_mod(Poly):
    # This checks commutation, not numerical correctness
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    c3 = list(random((2,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = Poly(c3)
    p4 = p1 * p2 + p3
    c4 = list(p4.coef)
    assert_poly_almost_equal(p4 % p2, p3)
    assert_poly_almost_equal(p4 % c2, p3)
    assert_poly_almost_equal(c4 % p2, p3)
    assert_poly_almost_equal(p4 % tuple(c2), p3)
    assert_poly_almost_equal(tuple(c4) % p2, p3)
    assert_poly_almost_equal(p4 % np.array(c2), p3)
    assert_poly_almost_equal(np.array(c4) % p2, p3)
    assert_poly_almost_equal(2 % p2, Poly([2]))
    assert_poly_almost_equal(p2 % 2, Poly([0]))
    assert_raises(TypeError, op.mod, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(TypeError, op.mod, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, op.mod, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, op.mod, p1, Polynomial([0]))


def test_mod():
    mp.dps = 15
    assert mpf(234) % 1 == 0
    assert mpf(-3) % 256 == 253
    assert mpf(0.25) % 23490.5 == 0.25
    assert mpf(0.25) % -23490.5 == -23490.25
    assert mpf(-0.25) % 23490.5 == 23490.25
    assert mpf(-0.25) % -23490.5 == -0.25
    # Check that these cases are handled efficiently
    assert mpf('1e10000000000') % 1 == 0
    assert mpf('1.23e-1000000000') % 1 == mpf('1.23e-1000000000')
    # test __rmod__
    assert 3 % mpf('1.75') == 1.25

