
def test_mul():
    from sympy.abc import x
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b, c, d = tensor_indices('a,b,c,d', Lorentz)
    t = TensMul.from_data(S.One, [], [], [])
    assert str(t) == '1'
    A, B = tensor_heads('A B', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = (1 + x)*A(a, b)
    assert str(t) == '(x + 1)*A(a, b)'
    assert t.index_types == [Lorentz, Lorentz]
    assert t.rank == 2
    assert t.dum == []
    assert t.coeff == 1 + x
    assert sorted(t.free) == [(a, 0), (b, 1)]
    assert t.components == [A]

    ts = A(a, b)
    assert str(ts) == 'A(a, b)'
    assert ts.index_types == [Lorentz, Lorentz]
    assert ts.rank == 2
    assert ts.dum == []
    assert ts.coeff == 1
    assert sorted(ts.free) == [(a, 0), (b, 1)]
    assert ts.components == [A]

    t = A(-b, a)*B(-a, c)*A(-c, d)
    t1 = tensor_mul(*t.split())
    assert t == t1
    assert tensor_mul(*[]) == TensMul.from_data(S.One, [], [], [])

    t = TensMul.from_data(1, [], [], [])
    C = TensorHead('C', [])
    assert str(C()) == 'C'
    assert str(t) == '1'
    assert t == 1
    raises(ValueError, lambda: A(a, b)*A(a, c))


def test_mul():
    x, y, a, b, c = map(Symbol, 'xyabc')
    p, q = map(Wild, 'pq')

    e = 4*x
    assert e.match(p*x) == {p: 4}
    assert e.match(p*y) is None
    assert e.match(e + p*y) == {p: 0}

    e = a*x*b*c
    assert e.match(p*x) == {p: a*b*c}
    assert e.match(c*p*x) == {p: a*b}

    e = (a + b)*(a + c)
    assert e.match((p + b)*(p + c)) == {p: a}

    e = x
    assert e.match(p*x) == {p: 1}

    e = exp(x)
    assert e.match(x**p*exp(x*q)) == {p: 0, q: 1}

    e = I*Poly(x, x)
    assert e.match(I*p) == {p: x}


def test_mul():
    assert h*l == h*x == 1
    assert l*h == x*h == 2
    assert x*l == l*x == -x


def test_mul():
    x, y, z, a, b, c = symbols('x y z a b c')
    A, B, C = symbols('A B C', commutative=0)
    assert (x*y*z).subs(z*x, y) == y**2
    assert (z*x).subs(1/x, z) == 1
    assert (x*y/z).subs(1/z, a) == a*x*y
    assert (x*y/z).subs(x/z, a) == a*y
    assert (x*y/z).subs(y/z, a) == a*x
    assert (x*y/z).subs(x/z, 1/a) == y/a
    assert (x*y/z).subs(x, 1/a) == y/(z*a)
    assert (2*x*y).subs(5*x*y, z) != z*Rational(2, 5)
    assert (x*y*A).subs(x*y, a) == a*A
    assert (x**2*y**(x*Rational(3, 2))).subs(x*y**(x/2), 2) == 4*y**(x/2)
    assert (x*exp(x*2)).subs(x*exp(x), 2) == 2*exp(x)
    assert ((x**(2*y))**3).subs(x**y, 2) == 64
    assert (x*A*B).subs(x*A, y) == y*B
    assert (x*y*(1 + x)*(1 + x*y)).subs(x*y, 2) == 6*(1 + x)
    assert ((1 + A*B)*A*B).subs(A*B, x*A*B)
    assert (x*a/z).subs(x/z, A) == a*A
    assert (x**3*A).subs(x**2*A, a) == a*x
    assert (x**2*A*B).subs(x**2*B, a) == a*A
    assert (x**2*A*B).subs(x**2*A, a) == a*B
    assert (b*A**3/(a**3*c**3)).subs(a**4*c**3*A**3/b**4, z) == \
        b*A**3/(a**3*c**3)
    assert (6*x).subs(2*x, y) == 3*y
    assert (y*exp(x*Rational(3, 2))).subs(y*exp(x), 2) == 2*exp(x/2)
    assert (y*exp(x*Rational(3, 2))).subs(y*exp(x), 2) == 2*exp(x/2)
    assert (A**2*B*A**2*B*A**2).subs(A*B*A, C) == A*C**2*A
    assert (x*A**3).subs(x*A, y) == y*A**2
    assert (x**2*A**3).subs(x*A, y) == y**2*A
    assert (x*A**3).subs(x*A, B) == B*A**2
    assert (x*A*B*A*exp(x*A*B)).subs(x*A, B) == B**2*A*exp(B*B)
    assert (x**2*A*B*A*exp(x*A*B)).subs(x*A, B) == B**3*exp(B**2)
    assert (x**3*A*exp(x*A*B)*A*exp(x*A*B)).subs(x*A, B) == \
        x*B*exp(B**2)*B*exp(B**2)
    assert (x*A*B*C*A*B).subs(x*A*B, C) == C**2*A*B
    assert (-I*a*b).subs(a*b, 2) == -2*I

    # issue 6361
    assert (-8*I*a).subs(-2*a, 1) == 4*I
    assert (-I*a).subs(-a, 1) == I

    # issue 6441
    assert (4*x**2).subs(2*x, y) == y**2
    assert (2*4*x**2).subs(2*x, y) == 2*y**2
    assert (-x**3/9).subs(-x/3, z) == -z**2*x
    assert (-x**3/9).subs(x/3, z) == -z**2*x
    assert (-2*x**3/9).subs(x/3, z) == -2*x*z**2
    assert (-2*x**3/9).subs(-x/3, z) == -2*x*z**2
    assert (-2*x**3/9).subs(-2*x, z) == z*x**2/9
    assert (-2*x**3/9).subs(2*x, z) == -z*x**2/9
    assert (2*(3*x/5/7)**2).subs(3*x/5, z) == 2*(Rational(1, 7))**2*z**2
    assert (4*x).subs(-2*x, z) == 4*x  # try keep subs literal


def test_mul():
    a, b = [0, 2, 1, 3], [0, 1, 3, 2]
    assert _af_rmul(a, b) == [0, 2, 3, 1]
    assert _af_rmuln(a, b, list(range(4))) == [0, 2, 3, 1]
    assert rmul(Permutation(a), Permutation(b)).array_form == [0, 2, 3, 1]

    a = Permutation([0, 2, 1, 3])
    b = (0, 1, 3, 2)
    c = (3, 1, 2, 0)
    assert Permutation.rmul(a, b, c) == Permutation([1, 2, 3, 0])
    assert Permutation.rmul(a, c) == Permutation([3, 2, 1, 0])
    raises(TypeError, lambda: Permutation.rmul(b, c))

    n = 6
    m = 8
    a = [Permutation.unrank_nonlex(n, i).array_form for i in range(m)]
    h = list(range(n))
    for i in range(m):
        h = _af_rmul(h, a[i])
        h2 = _af_rmuln(*a[:i + 1])
        assert h == h2


def test_mul(any_string_dtype):
    dtype = any_string_dtype
    a = pd.array(["a", "b", None], dtype=dtype)
    result = a * 2
    expected = pd.array(["aa", "bb", None], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

    result = 2 * a
    tm.assert_extension_array_equal(result, expected)


def test_mul(Poly):
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = p1 * p2
    assert_poly_almost_equal(p2 * p1, p3)
    assert_poly_almost_equal(p1 * c2, p3)
    assert_poly_almost_equal(c2 * p1, p3)
    assert_poly_almost_equal(p1 * tuple(c2), p3)
    assert_poly_almost_equal(tuple(c2) * p1, p3)
    assert_poly_almost_equal(p1 * np.array(c2), p3)
    assert_poly_almost_equal(np.array(c2) * p1, p3)
    assert_poly_almost_equal(p1 * 2, p1 * Poly([2]))
    assert_poly_almost_equal(2 * p1, p1 * Poly([2]))
    assert_raises(TypeError, op.mul, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(TypeError, op.mul, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, op.mul, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, op.mul, p1, Polynomial([0]))


def test_mul():
    assert mpf(2.5) * mpf(3) == 7.5
    assert mpf(2.5) * 3 == 7.5
    assert mpf(2.5) * 3.0 == 7.5
    assert 3 * mpf(2.5) == 7.5
    assert 3.0 * mpf(2.5) == 7.5
    assert (3+0j) * mpf(2.5) == 7.5
    assert mpc(2.5) * mpf(3) == 7.5
    assert mpc(2.5) * 3 == 7.5
    assert mpc(2.5) * 3.0 == 7.5
    assert mpc(2.5) * (3+0j) == 7.5
    assert 3 * mpc(2.5) == 7.5
    assert 3.0 * mpc(2.5) == 7.5
    assert (3+0j) * mpc(2.5) == 7.5

