
def test_add():
    per = SeqPer((1, 2), (n, 0, oo))
    form = SeqFormula(n**2)

    assert per + (SeqPer((2, 3))) == SeqPer((3, 5), (n, 0, oo))
    assert form + SeqFormula(n**3) == SeqFormula(n**2 + n**3)

    assert per + form == SeqAdd(per, form)

    raises(TypeError, lambda: per + n)
    raises(TypeError, lambda: n + per)


def test_add():
    expr = x + y
    comp = aesara_code_(expr)
    assert comp.owner.op == aesara.tensor.add


def test_add():
    expr = x + y
    comp = theano_code_(expr)
    assert comp.owner.op == theano.tensor.add


def test_add():
    m = ArithmeticOnlyMatrix([[1, 2, 3], [x, y, x], [2*y, -50, z*x]])
    assert m + m == ArithmeticOnlyMatrix([[2, 4, 6], [2*x, 2*y, 2*x], [4*y, -100, 2*z*x]])
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    raises(ShapeError, lambda: m + n)


def test_add():
    m = Matrix([[1, 2, 3], [x, y, x], [2*y, -50, z*x]])
    assert m + m == Matrix([[2, 4, 6], [2*x, 2*y, 2*x], [4*y, -100, 2*z*x]])
    n = Matrix(1, 2, [1, 2])
    raises(ShapeError, lambda: m + n)


def test_add():
    assert SparseMatrix(((1, 0), (0, 1))) + SparseMatrix(((0, 1), (1, 0))) == \
        SparseMatrix(((1, 1), (1, 1)))
    a = SparseMatrix(100, 100, lambda i, j: int(j != 0 and i % j == 0))
    b = SparseMatrix(100, 100, lambda i, j: int(i != 0 and j % i == 0))
    assert (len(a.todok()) + len(b.todok()) - len((a + b).todok()) > 0)


def test_add():
    x, y, a, b, c = map(Symbol, 'xyabc')
    p, q, r = map(Wild, 'pqr')

    e = a + b
    assert e.match(p + b) == {p: a}
    assert e.match(p + a) == {p: b}

    e = 1 + b
    assert e.match(p + b) == {p: 1}

    e = a + b + c
    assert e.match(a + p + c) == {p: b}
    assert e.match(b + p + c) == {p: a}

    e = a + b + c + x
    assert e.match(a + p + x + c) == {p: b}
    assert e.match(b + p + c + x) == {p: a}
    assert e.match(b) is None
    assert e.match(b + p) == {p: a + c + x}
    assert e.match(a + p + c) == {p: b + x}
    assert e.match(b + p + c) == {p: a + x}

    e = 4*x + 5
    assert e.match(4*x + p) == {p: 5}
    assert e.match(3*x + p) == {p: x + 5}
    assert e.match(p*x + 5) == {p: 4}


def test_add():
    with evaluate(False):
        p = oo - oo
        assert isinstance(p, Add) and p.args == (oo, -oo)
        p = 5 - oo
        assert isinstance(p, Add) and p.args == (-oo, 5)
        p = oo - 5
        assert isinstance(p, Add) and p.args == (oo, -5)
        p = oo + 5
        assert isinstance(p, Add) and p.args == (oo, 5)
        p = 5 + oo
        assert isinstance(p, Add) and p.args == (oo, 5)
        p = -oo + 5
        assert isinstance(p, Add) and p.args == (-oo, 5)
        p = -5 - oo
        assert isinstance(p, Add) and p.args == (-oo, -5)

    with evaluate(False):
        expr = x + x
        assert isinstance(expr, Add)
        assert expr.args == (x, x)

        with evaluate(True):
            assert (x + x).args == (2, x)

        assert (x + x).args == (x, x)

    assert isinstance(x + x, Mul)

    with evaluate(False):
        assert S.One + 1 == Add(1, 1)
        assert 1 + S.One == Add(1, 1)

        assert S(4) - 3 == Add(4, -3)
        assert -3 + S(4) == Add(4, -3)

        assert S(2) * 4 == Mul(2, 4)
        assert 4 * S(2) == Mul(2, 4)

        assert S(6) / 3 == Mul(6, Pow(3, -1))
        assert S.One / 3 * 6 == Mul(S.One / 3, 6)

        assert 9 ** S(2) == Pow(9, 2)
        assert S(2) ** 9 == Pow(2, 9)

        assert S(2) / 2 == Mul(2, Pow(2, -1))
        assert S.One / 2 * 2 == Mul(S.One / 2, 2)

        assert S(2) / 3 + 1 == Add(S(2) / 3, 1)
        assert 1 + S(2) / 3 == Add(1, S(2) / 3)

        assert S(4) / 7 - 3 == Add(S(4) / 7, -3)
        assert -3 + S(4) / 7 == Add(-3, S(4) / 7)

        assert S(2) / 4 * 4 == Mul(S(2) / 4, 4)
        assert 4 * (S(2) / 4) == Mul(4, S(2) / 4)

        assert S(6) / 3 == Mul(6, Pow(3, -1))
        assert S.One / 3 * 6 == Mul(S.One / 3, 6)

        assert S.One / 3 + sqrt(3) == Add(S.One / 3, sqrt(3))
        assert sqrt(3) + S.One / 3 == Add(sqrt(3), S.One / 3)

        assert S.One / 2 * 10.333 == Mul(S.One / 2, 10.333)
        assert 10.333 * (S.One / 2) == Mul(10.333, S.One / 2)

        assert sqrt(2) * sqrt(2) == Mul(sqrt(2), sqrt(2))

        assert S.One / 2 + x == Add(S.One / 2, x)
        assert x + S.One / 2 == Add(x, S.One / 2)

        assert S.One / x * x == Mul(S.One / x, x)
        assert x * (S.One / x) == Mul(x, Pow(x, -1))

        assert S.One / 3 == Pow(3, -1)
        assert S.One / x == Pow(x, -1)
        assert 1 / S(3) == Pow(3, -1)
        assert 1 / x == Pow(x, -1)


def test_add():
    assert h + l == h + x == 1
    assert l + h == x + h == 2
    assert x + l == l + x == x - 1


def test_add():
    a, b, c, d, x, y, t = symbols('a b c d x y t')

    assert (a**2 - b - c).subs(a**2 - b, d) in [d - c, a**2 - b - c]
    assert (a**2 - c).subs(a**2 - c, d) == d
    assert (a**2 - b - c).subs(a**2 - c, d) in [d - b, a**2 - b - c]
    assert (a**2 - x - c).subs(a**2 - c, d) in [d - x, a**2 - x - c]
    assert (a**2 - b - sqrt(a)).subs(a**2 - sqrt(a), c) == c - b
    assert (a + b + exp(a + b)).subs(a + b, c) == c + exp(c)
    assert (c + b + exp(c + b)).subs(c + b, a) == a + exp(a)
    assert (a + b + c + d).subs(b + c, x) == a + d + x
    assert (a + b + c + d).subs(-b - c, x) == a + d - x
    assert ((x + 1)*y).subs(x + 1, t) == t*y
    assert ((-x - 1)*y).subs(x + 1, t) == -t*y
    assert ((x - 1)*y).subs(x + 1, t) == y*(t - 2)
    assert ((-x + 1)*y).subs(x + 1, t) == y*(-t + 2)

    # this should work every time:
    e = a**2 - b - c
    assert e.subs(Add(*e.args[:2]), d) == d + e.args[2]
    assert e.subs(a**2 - c, d) == d - b

    # the fallback should recognize when a change has
    # been made; while .1 == Rational(1, 10) they are not the same
    # and the change should be made
    assert (0.1 + a).subs(0.1, Rational(1, 10)) == Rational(1, 10) + a

    e = (-x*(-y + 1) - y*(y - 1))
    ans = (-x*(x) - y*(-x)).expand()
    assert e.subs(-y + 1, x) == ans

    #Test issue 18747
    assert (exp(x) + cos(x)).subs(x, oo) == oo
    assert Add(*[AccumBounds(-1, 1), oo]) == oo
    assert Add(*[oo, AccumBounds(-1, 1)]) == oo


def test_add(n):
    elements = get_elements(n)
    dis1 = DisjointSet(elements)

    dis2 = DisjointSet()
    for i, x in enumerate(elements):
        dis2.add(x)
        assert len(dis2) == i + 1

        # test idempotency by adding element again
        dis2.add(x)
        assert len(dis2) == i + 1

    assert list(dis1) == list(dis2)


def test_add(any_string_dtype, request):
    dtype = any_string_dtype
    if dtype == object:
        mark = pytest.mark.xfail(
            reason="Need to update expected for numpy object dtype"
        )
        request.applymarker(mark)

    a = Series(["a", "b", "c", None, None], dtype=dtype)
    b = Series(["x", "y", None, "z", None], dtype=dtype)

    result = a + b
    expected = Series(["ax", "by", None, None, None], dtype=dtype)
    tm.assert_series_equal(result, expected)

    result = a.add(b)
    tm.assert_series_equal(result, expected)

    result = a.radd(b)
    expected = Series(["xa", "yb", None, None, None], dtype=dtype)
    tm.assert_series_equal(result, expected)

    result = a.add(b, fill_value="-")
    expected = Series(["ax", "by", "c-", "-z", None], dtype=dtype)
    tm.assert_series_equal(result, expected)


def test_add(Poly):
    # This checks commutation, not numerical correctness
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = p1 + p2
    assert_poly_almost_equal(p2 + p1, p3)
    assert_poly_almost_equal(p1 + c2, p3)
    assert_poly_almost_equal(c2 + p1, p3)
    assert_poly_almost_equal(p1 + tuple(c2), p3)
    assert_poly_almost_equal(tuple(c2) + p1, p3)
    assert_poly_almost_equal(p1 + np.array(c2), p3)
    assert_poly_almost_equal(np.array(c2) + p1, p3)
    assert_raises(TypeError, op.add, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(TypeError, op.add, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, op.add, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, op.add, p1, Polynomial([0]))


def test_add():
    assert mpf(2.5) + mpf(3) == 5.5
    assert mpf(2.5) + 3 == 5.5
    assert mpf(2.5) + 3.0 == 5.5
    assert 3 + mpf(2.5) == 5.5
    assert 3.0 + mpf(2.5) == 5.5
    assert (3+0j) + mpf(2.5) == 5.5
    assert mpc(2.5) + mpf(3) == 5.5
    assert mpc(2.5) + 3 == 5.5
    assert mpc(2.5) + 3.0 == 5.5
    assert mpc(2.5) + (3+0j) == 5.5
    assert 3 + mpc(2.5) == 5.5
    assert 3.0 + mpc(2.5) == 5.5
    assert (3+0j) + mpc(2.5) == 5.5

