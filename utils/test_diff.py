
def test_diff():
    assert raises(TypeError, lambda: list(diff()))
    assert raises(TypeError, lambda: list(diff([1, 2])))
    assert raises(TypeError, lambda: list(diff([1, 2], 3)))
    assert list(diff([1, 2], (1, 2), iter([1, 2]))) == []
    assert list(diff([1, 2, 3], (1, 10, 3), iter([1, 2, 10]))) == [
        (2, 10, 2), (3, 3, 10)]
    assert list(diff([1, 2], [10])) == [(1, 10)]
    assert list(diff([1, 2], [10], default=None)) == [(1, 10), (2, None)]
    # non-variadic usage
    assert raises(TypeError, lambda: list(diff([])))
    assert raises(TypeError, lambda: list(diff([[]])))
    assert raises(TypeError, lambda: list(diff([[1, 2]])))
    assert raises(TypeError, lambda: list(diff([[1, 2], 3])))
    assert list(diff([(1, 2), (1, 3)])) == [(2, 3)]

    data1 = [{'cost': 1, 'currency': 'dollar'},
             {'cost': 2, 'currency': 'dollar'}]

    data2 = [{'cost': 100, 'currency': 'yen'},
             {'cost': 300, 'currency': 'yen'}]

    conversions = {'dollar': 1, 'yen': 0.01}

    def indollars(item):
        return conversions[item['currency']] * item['cost']

    list(diff(data1, data2, key=indollars)) == [
        ({'cost': 2, 'currency': 'dollar'}, {'cost': 300, 'currency': 'yen'})]


def test_diff():
    from sympy.abc import x, y, z
    md = MutableDenseNDimArray([[x, y], [x*z, x*y*z]])
    assert md.diff(x) == MutableDenseNDimArray([[1, 0], [z, y*z]])
    assert diff(md, x) == MutableDenseNDimArray([[1, 0], [z, y*z]])

    sd = MutableSparseNDimArray(md)
    assert sd == MutableSparseNDimArray([x, y, x*z, x*y*z], (2, 2))
    assert sd.diff(x) == MutableSparseNDimArray([[1, 0], [z, y*z]])
    assert diff(sd, x) == MutableSparseNDimArray([[1, 0], [z, y*z]])


def test_diff():
    x = Symbol("x")
    y = Symbol("y")
    f = Function("f")
    g = Function("g")
    assert simplify(g(x).diff(x)*f(x).diff(x) - f(x).diff(x)*g(x).diff(x)) == 0
    assert simplify(2*f(x)*f(x).diff(x) - diff(f(x)**2, x)) == 0
    assert simplify(diff(1/f(x), x) + f(x).diff(x)/f(x)**2) == 0
    assert simplify(f(x).diff(x, y) - f(x).diff(y, x)) == 0


def test_diff():
    assert O(x**2).diff(x) == O(x)


def test_diff():
    x, y = symbols('x y')
    m = CalculusOnlyMatrix(2, 1, [x, y])
    # TODO: currently not working as ``_MinimalMatrix`` cannot be sympified:
    assert m.diff(x) == Matrix(2, 1, [1, 0])


def test_diff():
    A = MutableDenseMatrix(((1, 4, x), (y, 2, 4), (10, 5, x**2 + 1)))
    assert isinstance(A.diff(x), type(A))
    assert A.diff(x) == MutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert A.diff(y) == MutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert diff(A, x) == MutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert diff(A, y) == MutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    A_imm = A.as_immutable()
    assert isinstance(A_imm.diff(x), type(A_imm))
    assert A_imm.diff(x) == ImmutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert A_imm.diff(y) == ImmutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert diff(A_imm, x) == ImmutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert diff(A_imm, y) == ImmutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert A.diff(x, evaluate=False) == ArrayDerivative(A, x, evaluate=False)
    assert diff(A, x, evaluate=False) == ArrayDerivative(A, x, evaluate=False)


def test_diff():
    A = MutableDenseMatrix(((1, 4, x), (y, 2, 4), (10, 5, x**2 + 1)))
    assert isinstance(A.diff(x), type(A))
    assert A.diff(x) == MutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert A.diff(y) == MutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert diff(A, x) == MutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert diff(A, y) == MutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    A_imm = A.as_immutable()
    assert isinstance(A_imm.diff(x), type(A_imm))
    assert A_imm.diff(x) == ImmutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert A_imm.diff(y) == ImmutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert diff(A_imm, x) == ImmutableDenseMatrix(((0, 0, 1), (0, 0, 0), (0, 0, 2*x)))
    assert diff(A_imm, y) == ImmutableDenseMatrix(((0, 0, 0), (1, 0, 0), (0, 0, 0)))

    assert A.diff(x, evaluate=False) == ArrayDerivative(A, x, evaluate=False)
    assert diff(A, x, evaluate=False) == ArrayDerivative(A, x, evaluate=False)


def test_diff():
    x, y = symbols('x, y')
    R, Dx = DifferentialOperators(ZZ.old_poly_ring(x), 'Dx')
    p = HolonomicFunction(x*Dx**2 + 1, x, 0, [0, 1])
    assert p.diff().to_expr() == p.to_expr().diff().simplify()
    p = HolonomicFunction(Dx**2 - 1, x, 0, [1, 0])
    assert p.diff(x, 2).to_expr() == p.to_expr()
    p = expr_to_holonomic(Si(x))
    assert p.diff().to_expr() == sin(x)/x
    assert p.diff(y) == 0
    C_0, C_1, C_2, C_3 = symbols('C_0, C_1, C_2, C_3')
    q = Si(x)
    assert p.diff(x).to_expr() == q.diff()
    assert p.diff(x, 2).to_expr().subs(C_0, Rational(-1, 3)).cancel() == q.diff(x, 2).cancel()
    assert p.diff(x, 3).series().subs({C_3: Rational(-1, 3), C_0: 0}) == q.diff(x, 3).series()


def test_diff():
    assert besselj(n, z).diff(z) == besselj(n - 1, z)/2 - besselj(n + 1, z)/2
    assert bessely(n, z).diff(z) == bessely(n - 1, z)/2 - bessely(n + 1, z)/2
    assert besseli(n, z).diff(z) == besseli(n - 1, z)/2 + besseli(n + 1, z)/2
    assert besselk(n, z).diff(z) == -besselk(n - 1, z)/2 - besselk(n + 1, z)/2
    assert hankel1(n, z).diff(z) == hankel1(n - 1, z)/2 - hankel1(n + 1, z)/2
    assert hankel2(n, z).diff(z) == hankel2(n - 1, z)/2 - hankel2(n + 1, z)/2


def test_diff():
    assert Rational(1, 3).diff(x) is S.Zero
    assert I.diff(x) is S.Zero
    assert pi.diff(x) is S.Zero
    assert x.diff(x, 0) == x
    assert (x**2).diff(x, 2, x) == 0
    assert (x**2).diff((x, 2), x) == 0
    assert (x**2).diff((x, 1), x) == 2
    assert (x**2).diff((x, 1), (x, 1)) == 2
    assert (x**2).diff((x, 2)) == 2
    assert (x**2).diff(x, y, 0) == 2*x
    assert (x**2).diff(x, (y, 0)) == 2*x
    assert (x**2).diff(x, y) == 0
    raises(ValueError, lambda: x.diff(1, x))

    p = Rational(5)
    e = a*b + b**p
    assert e.diff(a) == b
    assert e.diff(b) == a + 5*b**4
    assert e.diff(b).diff(a) == Rational(1)
    e = a*(b + c)
    assert e.diff(a) == b + c
    assert e.diff(b) == a
    assert e.diff(b).diff(a) == Rational(1)
    e = c**p
    assert e.diff(c, 6) == Rational(0)
    assert e.diff(c, 5) == Rational(120)
    e = c**Rational(2)
    assert e.diff(c) == 2*c
    e = a*b*c
    assert e.diff(c) == a*b


def test_diff():
    assert Sum(x, (x, 1, 2)).diff(x) == 0
    assert Sum(x*y, (x, 1, 2)).diff(x) == 0
    assert Sum(x*y, (y, 1, 2)).diff(x) == Sum(y, (y, 1, 2))
    e = Sum(x*y, (x, 1, a))
    assert e.diff(a) == Derivative(e, a)
    assert Sum(x*y, (x, 1, 3), (a, 2, 5)).diff(y).doit() == \
        Sum(x*y, (x, 1, 3), (a, 2, 5)).doit().diff(y) == 24
    assert Sum(x, (x, 1, 2)).diff(y) == 0


def test_diff():
    df = DataFrame({"a": [1, 2, 3], "b": 1.5})

    result = df.diff()
    assert result.index is not df.index
    assert result.columns is not df.columns

    ser = Series([1, 2, 3])
    result = ser.diff()
    assert result.index is not ser.index


def test_diff():
    a = pd.array(
        [True, True, False, False, True, None, True, None, False], dtype="boolean"
    )
    result = pd.core.algorithms.diff(a, 1)
    expected = pd.array(
        [None, False, True, False, True, None, None, None, None], dtype="boolean"
    )
    tm.assert_extension_array_equal(result, expected)

    ser = pd.Series(a)
    result = ser.diff()
    expected = pd.Series(expected)
    tm.assert_series_equal(result, expected)


def test_diff():
    ser = pd.Series([1, 2, 3], dtype="category")

    msg = "Convert to a suitable dtype"
    with pytest.raises(TypeError, match=msg):
        ser.diff()

    df = ser.to_frame(name="A")
    with pytest.raises(TypeError, match=msg):
        df.diff()


def test_diff():
    mp.dps = 15
    assert diff(log, 2.0, n=0).ae(log(2))
    assert diff(cos, 1.0).ae(-sin(1))
    assert diff(abs, 0.0) == 0
    assert diff(abs, 0.0, direction=1) == 1
    assert diff(abs, 0.0, direction=-1) == -1
    assert diff(exp, 1.0).ae(e)
    assert diff(exp, 1.0, n=5).ae(e)
    assert diff(exp, 2.0, n=5, direction=3*j).ae(e**2)
    assert diff(lambda x: x**2, 3.0, method='quad').ae(6)
    assert diff(lambda x: 3+x**5, 3.0, n=2, method='quad').ae(540)
    assert diff(lambda x: 3+x**5, 3.0, n=2, method='step').ae(540)
    assert diffun(sin)(2).ae(cos(2))
    assert diffun(sin, n=2)(2).ae(-sin(2))


def test_diff():
    a = A()
    b = A()
    c = A()
    a.a = b
    b.a = c
    diff.memorise(a)
    assert not diff.has_changed(a)
    c.a = 1
    assert diff.has_changed(a)
    diff.memorise(c, force=True)
    assert not diff.has_changed(a)
    c.a = 2
    assert diff.has_changed(a)
    changed = diff.whats_changed(a)
    assert list(changed[0].keys()) == ["a"]
    assert not changed[1]

    a2 = []
    b2 = [a2]
    c2 = [b2]
    diff.memorise(c2)
    assert not diff.has_changed(c2)
    a2.append(1)
    assert diff.has_changed(c2)
    changed = diff.whats_changed(c2)
    assert changed[0] == {}
    assert changed[1]

    a3 = {}
    b3 = {1: a3}
    c3 = {1: b3}
    diff.memorise(c3)
    assert not diff.has_changed(c3)
    a3[1] = 1
    assert diff.has_changed(c3)
    changed = diff.whats_changed(c3)
    assert changed[0] == {}
    assert changed[1]

    if not IS_PYPY:
        import abc
        # make sure the "_abc_invaldation_counter" doesn't make test fail
        diff.memorise(abc.ABCMeta, force=True)
        assert not diff.has_changed(abc)
        abc.ABCMeta.zzz = 1
        assert diff.has_changed(abc)
        changed = diff.whats_changed(abc)
        assert list(changed[0].keys()) == ["ABCMeta"]
        assert not changed[1]

    '''
    import Queue
    diff.memorise(Queue, force=True)
    assert not diff.has_changed(Queue)
    Queue.Queue.zzz = 1
    assert diff.has_changed(Queue)
    changed = diff.whats_changed(Queue)
    assert list(changed[0].keys()) == ["Queue"]
    assert not changed[1]

    import math
    diff.memorise(math, force=True)
    assert not diff.has_changed(math)
    math.zzz = 1
    assert diff.has_changed(math)
    changed = diff.whats_changed(math)
    assert list(changed[0].keys()) == ["zzz"]
    assert not changed[1]
    '''

    a = A()
    b = A()
    c = A()
    a.a = b
    b.a = c
    diff.memorise(a)
    assert not diff.has_changed(a)
    c.a = 1
    assert diff.has_changed(a)
    diff.memorise(c, force=True)
    assert not diff.has_changed(a)
    del c.a
    assert diff.has_changed(a)
    changed = diff.whats_changed(a)
    assert list(changed[0].keys()) == ["a"]
    assert not changed[1]

