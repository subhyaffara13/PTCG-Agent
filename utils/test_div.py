
def test_div():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    m0, m1, m2, m3 = tensor_indices('m0:4', Lorentz)
    R = TensorHead('R', [Lorentz]*4, TensorSymmetry.riemann())
    t = R(m0,m1,-m1,m3)
    t1 = t/S(4)
    assert str(t1) == '(1/4)*R(m0, L_0, -L_0, m3)'
    t = t.canon_bp()
    assert not t1._is_canon_bp
    t1 = t*4
    assert t1._is_canon_bp
    t1 = t1/4
    assert t1._is_canon_bp


def test_div():
    f, g = x**2 - y**2, x - y
    q, r = x + y, 0

    F, G, Q, R = [ Poly(h, x, y) for h in (f, g, q, r) ]

    assert F.div(G) == (Q, R)
    assert F.rem(G) == R
    assert F.quo(G) == Q
    assert F.exquo(G) == Q

    assert div(f, g) == (q, r)
    assert rem(f, g) == r
    assert quo(f, g) == q
    assert exquo(f, g) == q

    assert div(f, g, x, y) == (q, r)
    assert rem(f, g, x, y) == r
    assert quo(f, g, x, y) == q
    assert exquo(f, g, x, y) == q

    assert div(f, g, (x, y)) == (q, r)
    assert rem(f, g, (x, y)) == r
    assert quo(f, g, (x, y)) == q
    assert exquo(f, g, (x, y)) == q

    assert div(F, G) == (Q, R)
    assert rem(F, G) == R
    assert quo(F, G) == Q
    assert exquo(F, G) == Q

    assert div(f, g, polys=True) == (Q, R)
    assert rem(f, g, polys=True) == R
    assert quo(f, g, polys=True) == Q
    assert exquo(f, g, polys=True) == Q

    assert div(F, G, polys=False) == (q, r)
    assert rem(F, G, polys=False) == r
    assert quo(F, G, polys=False) == q
    assert exquo(F, G, polys=False) == q

    raises(ComputationFailed, lambda: div(4, 2))
    raises(ComputationFailed, lambda: rem(4, 2))
    raises(ComputationFailed, lambda: quo(4, 2))
    raises(ComputationFailed, lambda: exquo(4, 2))

    f, g = x**2 + 1, 2*x - 4

    qz, rz = 0, x**2 + 1
    qq, rq = x/2 + 1, 5

    assert div(f, g) == (qq, rq)
    assert div(f, g, auto=True) == (qq, rq)
    assert div(f, g, auto=False) == (qz, rz)
    assert div(f, g, domain=ZZ) == (qz, rz)
    assert div(f, g, domain=QQ) == (qq, rq)
    assert div(f, g, domain=ZZ, auto=True) == (qq, rq)
    assert div(f, g, domain=ZZ, auto=False) == (qz, rz)
    assert div(f, g, domain=QQ, auto=True) == (qq, rq)
    assert div(f, g, domain=QQ, auto=False) == (qq, rq)

    assert rem(f, g) == rq
    assert rem(f, g, auto=True) == rq
    assert rem(f, g, auto=False) == rz
    assert rem(f, g, domain=ZZ) == rz
    assert rem(f, g, domain=QQ) == rq
    assert rem(f, g, domain=ZZ, auto=True) == rq
    assert rem(f, g, domain=ZZ, auto=False) == rz
    assert rem(f, g, domain=QQ, auto=True) == rq
    assert rem(f, g, domain=QQ, auto=False) == rq

    assert quo(f, g) == qq
    assert quo(f, g, auto=True) == qq
    assert quo(f, g, auto=False) == qz
    assert quo(f, g, domain=ZZ) == qz
    assert quo(f, g, domain=QQ) == qq
    assert quo(f, g, domain=ZZ, auto=True) == qq
    assert quo(f, g, domain=ZZ, auto=False) == qz
    assert quo(f, g, domain=QQ, auto=True) == qq
    assert quo(f, g, domain=QQ, auto=False) == qq

    f, g, q = x**2, 2*x, x/2

    assert exquo(f, g) == q
    assert exquo(f, g, auto=True) == q
    raises(ExactQuotientFailed, lambda: exquo(f, g, auto=False))
    raises(ExactQuotientFailed, lambda: exquo(f, g, domain=ZZ))
    assert exquo(f, g, domain=QQ) == q
    assert exquo(f, g, domain=ZZ, auto=True) == q
    raises(ExactQuotientFailed, lambda: exquo(f, g, domain=ZZ, auto=False))
    assert exquo(f, g, domain=QQ, auto=True) == q
    assert exquo(f, g, domain=QQ, auto=False) == q

    f, g = Poly(x**2), Poly(x)

    q, r = f.div(g)
    assert q.get_domain().is_ZZ and r.get_domain().is_ZZ
    r = f.rem(g)
    assert r.get_domain().is_ZZ
    q = f.quo(g)
    assert q.get_domain().is_ZZ
    q = f.exquo(g)
    assert q.get_domain().is_ZZ

    f, g = Poly(x+y, x), Poly(2*x+y, x)
    q, r = f.div(g)
    assert q.get_domain().is_Frac and r.get_domain().is_Frac

    # https://github.com/sympy/sympy/issues/19579
    p = Poly(2+3*I, x, domain=ZZ_I)
    q = Poly(1-I, x, domain=ZZ_I)
    assert p.div(q, auto=False) == \
        (Poly(0, x, domain='ZZ_I'), Poly(2 + 3*I, x, domain='ZZ_I'))
    assert p.div(q, auto=True) == \
        (Poly(-S(1)/2 + 5*I/2, x, domain='QQ_I'), Poly(0, x, domain='QQ_I'))

    f = 5*x**2 + 10*x + 3
    g = 2*x + 2
    assert div(f, g, domain=ZZ) == (0, f)


def test_div():
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    assert n/2 == ArithmeticOnlyMatrix(1, 2, [S.Half, S(2)/2])


def test_div():
    n = Matrix(1, 2, [1, 2])
    assert n/2 == Matrix(1, 2, [S.Half, S(2)/2])


def test_div():
    e = a/b
    assert e == a*b**(-1)
    e = a/b + c/2
    assert e == a*b**(-1) + Rational(1)/2*c
    e = (1 - b)/(b - 1)
    assert e == (1 + -b)*((-1) + b)**(-1)


def test_div():
    assert h/l == h/x == 1
    assert l/h == x/h == 2
    assert x/l == 1/(l/x) == -x


def test_div(left_array, right_array):
    msg = "operator '.*' not implemented for bool dtypes"
    with pytest.raises(NotImplementedError, match=msg):
        # check that we are matching the non-masked Series behavior
        pd.Series(left_array._data) / pd.Series(right_array._data)

    with pytest.raises(NotImplementedError, match=msg):
        left_array / right_array


def test_div(dtype):
    a = pd.array([1, 2, 3, None, 5], dtype=dtype)
    b = pd.array([0, 1, None, 3, 4], dtype=dtype)

    result = a / b
    expected = pd.array([np.inf, 2, None, None, 1.25], dtype="Float64")
    tm.assert_extension_array_equal(result, expected)


def test_div():
    assert mpf(6) / mpf(3) == 2.0
    assert mpf(6) / 3 == 2.0
    assert mpf(6) / 3.0 == 2.0
    assert 6 / mpf(3) == 2.0
    assert 6.0 / mpf(3) == 2.0
    assert (6+0j) / mpf(3.0) == 2.0
    assert mpc(6) / mpf(3) == 2.0
    assert mpc(6) / 3 == 2.0
    assert mpc(6) / 3.0 == 2.0
    assert mpc(6) / (3+0j) == 2.0
    assert 6 / mpc(3) == 2.0
    assert 6.0 / mpc(3) == 2.0
    assert (6+0j) / mpc(3) == 2.0

