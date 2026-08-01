
def test_series():
    e = Symbol("e")
    x = Symbol("x")
    for c in (Limit, Limit(e, x, 1), Order, Order(e)):
        check(c)


def test_series():
    C1 = Symbol("C1")
    eq = f(x).diff(x) - f(x)
    sol = Eq(f(x), C1 + C1*x + C1*x**2/2 + C1*x**3/6 + C1*x**4/24 +
            C1*x**5/120 + O(x**6))
    assert dsolve(eq, hint='1st_power_series') == sol
    assert checkodesol(eq, sol, order=1)[0]

    eq = f(x).diff(x) - x*f(x)
    sol = Eq(f(x), C1*x**4/8 + C1*x**2/2 + C1 + O(x**6))
    assert dsolve(eq, hint='1st_power_series') == sol
    assert checkodesol(eq, sol, order=1)[0]

    eq = f(x).diff(x) - sin(x*f(x))
    sol = Eq(f(x), (x - 2)**2*(1+ sin(4))*cos(4) + (x - 2)*sin(4) + 2 + O(x**3))
    assert dsolve(eq, hint='1st_power_series', ics={f(2): 2}, n=3) == sol


def test_series():
    from sympy.abc import x
    i = Integral(cos(x), (x, x))
    e = i.lseries(x)
    assert i.nseries(x, n=8).removeO() == Add(*[next(e) for j in range(4)])


def test_series():
    x = symbols('x')
    R, Dx = DifferentialOperators(ZZ.old_poly_ring(x), 'Dx')
    p = HolonomicFunction(Dx**2 + 2*x*Dx, x, 0, [0, 1]).series(n=10)
    q = x - x**3/3 + x**5/10 - x**7/42 + x**9/216 + O(x**10)
    assert p == q
    p = HolonomicFunction(Dx - 1, x).composition(x**2, 0, [1])  # e^(x**2)
    q = HolonomicFunction(Dx**2 + 1, x, 0, [1, 0])  # cos(x)
    r = (p * q).series(n=10)  # expansion of cos(x) * exp(x**2)
    s = 1 + x**2/2 + x**4/24 - 31*x**6/720 - 179*x**8/8064 + O(x**10)
    assert r == s
    t = HolonomicFunction((1 + x)*Dx**2 + Dx, x, 0, [0, 1])  # log(1 + x)
    r = (p * t + q).series(n=10)
    s = 1 + x - x**2 + 4*x**3/3 - 17*x**4/24 + 31*x**5/30 - 481*x**6/720 +\
     71*x**7/105 - 20159*x**8/40320 + 379*x**9/840 + O(x**10)
    assert r == s
    p = HolonomicFunction((6+6*x-3*x**2) - (10*x-3*x**2-3*x**3)*Dx + \
        (4-6*x**3+2*x**4)*Dx**2, x, 0, [0, 1]).series(n=7)
    q = x + x**3/6 - 3*x**4/16 + x**5/20 - 23*x**6/960 + O(x**7)
    assert p == q
    p = HolonomicFunction((6+6*x-3*x**2) - (10*x-3*x**2-3*x**3)*Dx + \
        (4-6*x**3+2*x**4)*Dx**2, x, 0, [1, 0]).series(n=7)
    q = 1 - 3*x**2/4 - x**3/4 - 5*x**4/32 - 3*x**5/40 - 17*x**6/384 + O(x**7)
    assert p == q
    p = expr_to_holonomic(erf(x) + x).series(n=10)
    C_3 = symbols('C_3')
    q = (erf(x) + x).series(n=10)
    assert p.subs(C_3, -2/(3*sqrt(pi))) == q
    assert expr_to_holonomic(sqrt(x**3 + x)).series(n=10) == sqrt(x**3 + x).series(n=10)
    assert expr_to_holonomic((2*x - 3*x**2)**Rational(1, 3)).series() == ((2*x - 3*x**2)**Rational(1, 3)).series()
    assert  expr_to_holonomic(sqrt(x**2-x)).series() == (sqrt(x**2-x)).series()
    assert expr_to_holonomic(cos(x)**2/x**2, y0={-2: [1, 0, -1]}).series(n=10) == (cos(x)**2/x**2).series(n=10)
    assert expr_to_holonomic(cos(x)**2/x**2, x0=1).series(n=10).together() == (cos(x)**2/x**2).series(n=10, x0=1).together()
    assert expr_to_holonomic(cos(x-1)**2/(x-1)**2, x0=1, y0={-2: [1, 0, -1]}).series(n=10) \
        == (cos(x-1)**2/(x-1)**2).series(x0=1, n=10)


def test_series():
    l = Symbol('l', positive=True)
    assert SingularityFunction(x, -3, 2).series(x) == x**2 + 6*x + 9
    assert SingularityFunction(x, -2, 1).series(x) == x + 2
    assert SingularityFunction(x, 0, 0).series(x) == 1
    assert SingularityFunction(x, 0, 0).series(x, dir='-') == 0
    assert SingularityFunction(x, 0, -1).series(x) == 0
    assert SingularityFunction(x, 0, -2).series(x) == 0
    assert SingularityFunction(x, 0, -3).series(x) == 0
    assert SingularityFunction(x, 0, -4).series(x) == 0
    assert (SingularityFunction(x + l, 0, 1)/2\
        - SingularityFunction(x + l, l/2, 1)\
        + SingularityFunction(x + l, l, 1)/2).nseries(x) == -x/2 + O(x**6)


def test_series():
    x, y = symbols('x,y')
    assert floor(x).nseries(x, y, 100) == floor(y)
    assert ceiling(x).nseries(x, y, 100) == ceiling(y)
    assert floor(x).nseries(x, pi, 100) == 3
    assert ceiling(x).nseries(x, pi, 100) == 4
    assert floor(x).nseries(x, 0, 100) == 0
    assert ceiling(x).nseries(x, 0, 100) == 1
    assert floor(-x).nseries(x, 0, 100) == -1
    assert ceiling(-x).nseries(x, 0, 100) == 0


def test_series():
    # Test grouped Series
    ser = pd.Series([1, 2, 3, 4, 5], index=["a", "a", "a", "b", "b"])
    grouped = ser.groupby(level=0)
    result = grouped._positional_selector[1:2]
    expected = pd.Series([2, 5], index=["a", "b"])

    tm.assert_series_equal(result, expected)


def test_series():
    return Series(
        np.random.default_rng(2).standard_normal(1000),
        index=date_range("1/1/2000", periods=1000),
    )


def test_series(last_val, infer_string):
    with option_context("future.infer_string", infer_string):
        ser = Series(["1", "-3.14", last_val])
        result = to_numeric(ser)

    expected = Series([1, -3.14, 7])
    tm.assert_series_equal(result, expected)


def test_series(raw, series):
    result = series.rolling(50).apply(f, raw=raw)
    assert isinstance(result, Series)
    tm.assert_almost_equal(result.iloc[-1], np.mean(series[-50:]))


def test_series(series, compare_func, roll_func, kwargs, step):
    result = getattr(series.rolling(50, step=step), roll_func)(**kwargs)
    assert isinstance(result, Series)
    end = range(0, len(series), step or 1)[-1] + 1
    tm.assert_almost_equal(result.iloc[-1], compare_func(series[end - 50 : end]))


def test_series(series, q, step):
    compare_func = partial(scoreatpercentile, per=q)
    result = series.rolling(50, step=step).quantile(q)
    assert isinstance(result, Series)
    end = range(0, len(series), step or 1)[-1] + 1
    tm.assert_almost_equal(result.iloc[-1], compare_func(series[end - 50 : end]))


def test_series(series, sp_func, roll_func):
    sp_stats = pytest.importorskip("scipy.stats")

    compare_func = partial(getattr(sp_stats, sp_func), bias=False)
    result = getattr(series.rolling(50), roll_func)()
    assert isinstance(result, Series)
    tm.assert_almost_equal(result.iloc[-1], compare_func(series[-50:]))


def test_series():
    # see gh-6407
    s = Series(date_range("20130101", "20130110"))
    inferred = frequencies.infer_freq(s)
    assert inferred == "D"


def test_series(data, index, expected):
    # GH#52897
    ser = Series(data, index=index)
    assert ser.size == expected
    assert isinstance(ser.size, int)


def test_series():
    buf = StringIO()
    s = pd.Series([1, 2, 3], name="foo")
    s.to_markdown(buf=buf)
    result = buf.getvalue()
    assert result == (
        "|    |   foo |\n|---:|------:|\n|  0 |     1 |\n|  1 |     2 |\n|  2 |     3 |"
    )


def test_series(temp_h5_path):
    s = Series(range(10), dtype="float64", index=[f"i_{i}" for i in range(10)])
    _check_roundtrip(s, tm.assert_series_equal, path=temp_h5_path)

    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    _check_roundtrip(ts, tm.assert_series_equal, path=temp_h5_path)

    ts2 = Series(ts.index, Index(ts.index))
    _check_roundtrip(ts2, tm.assert_series_equal, path=temp_h5_path)

    ts3 = Series(ts.values, Index(np.asarray(ts.index)))
    _check_roundtrip(
        ts3, tm.assert_series_equal, path=temp_h5_path, check_index_type=False
    )


def test_series() -> None:
    """Tests that Series accepts (unstructured) void ExtensionDtypes."""
    from uuid import uuid4

    s = pd.Series([u := uuid4()], dtype=UuidDtype(), name="s")
    assert str(u) in str(s)


def test_series(data, all_arithmetic_operators):
    data, scalar = data
    op = tm.get_op_from_name(all_arithmetic_operators)
    check_skip(data, all_arithmetic_operators)

    ser = pd.Series(data)

    others = [
        scalar,
        np.array([scalar] * len(data), dtype=data.dtype.numpy_dtype),
        pd.array([scalar] * len(data), dtype=data.dtype),
        pd.Series([scalar] * len(data), dtype=data.dtype),
    ]

    for other in others:
        if is_bool_not_implemented(data, all_arithmetic_operators):
            msg = "operator '.*' not implemented for bool dtypes"
            with pytest.raises(NotImplementedError, match=msg):
                op(ser, other)

        else:
            result = op(ser, other)
            expected = pd.Series(op(data, other))
            tm.assert_series_equal(result, expected)

