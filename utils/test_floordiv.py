
def test_floordiv():
    from sympy.functions.elementary.integers import floor
    assert x // y == floor(x / y)


def test_floordiv():
    assert S(2)//S.Half == 4


def test_floordiv():
    assert h//l == h//x == 1
    assert l//h == x//h == 2
    assert x//l == floor(-x)
    assert l//x == floor(-1/x)


def test_floordiv(dtype):
    a = pd.array([1, 2, 3, None, 5], dtype=dtype)
    b = pd.array([0, 1, None, 3, 4], dtype=dtype)

    result = a // b
    # Series op sets 1//0 to np.inf, which IntegerArray does not do (yet)
    expected = pd.array([0, 2, None, None, 1], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)


def test_floordiv(Poly):
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    c3 = list(random((2,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = Poly(c3)
    p4 = p1 * p2 + p3
    c4 = list(p4.coef)
    assert_poly_almost_equal(p4 // p2, p1)
    assert_poly_almost_equal(p4 // c2, p1)
    assert_poly_almost_equal(c4 // p2, p1)
    assert_poly_almost_equal(p4 // tuple(c2), p1)
    assert_poly_almost_equal(tuple(c4) // p2, p1)
    assert_poly_almost_equal(p4 // np.array(c2), p1)
    assert_poly_almost_equal(np.array(c4) // p2, p1)
    assert_poly_almost_equal(2 // p2, Poly([0]))
    assert_poly_almost_equal(p2 // 2, 0.5 * p2)
    assert_raises(
        TypeError, op.floordiv, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(
        TypeError, op.floordiv, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, op.floordiv, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, op.floordiv, p1, Polynomial([0]))

