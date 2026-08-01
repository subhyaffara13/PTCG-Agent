
def test_str(doc):
    assert m.str_from_char_ssize_t().encode().decode() == "red"
    assert m.str_from_char_size_t().encode().decode() == "blue"
    assert m.str_from_string().encode().decode() == "baz"
    assert m.str_from_bytes().encode().decode() == "boo"

    assert doc(m.str_from_bytes) == "str_from_bytes() -> str"

    class A:
        def __str__(self):
            return "this is a str"

        def __repr__(self):
            return "this is a repr"

    assert m.str_from_object(A()) == "this is a str"
    assert m.repr_from_object(A()) == "this is a repr"
    assert m.str_from_handle(A()) == "this is a str"

    s1, s2 = m.str_format()
    assert s1 == "1 + 2 = 3"
    assert s1 == s2

    malformed_utf8 = b"\x80"
    if hasattr(m, "PYBIND11_STR_LEGACY_PERMISSIVE"):
        assert m.str_from_object(malformed_utf8) is malformed_utf8
    else:
        assert m.str_from_object(malformed_utf8) == "b'\\x80'"
    assert m.str_from_handle(malformed_utf8) == "b'\\x80'"

    assert m.str_from_string_from_str("this is a str") == "this is a str"
    ucs_surrogates_str = "\udcc3"
    with pytest.raises(UnicodeEncodeError):
        m.str_from_string_from_str(ucs_surrogates_str)


def test_str():
    # Without alias:
    k = QQ.alg_field_from_poly(Poly(x**2 + 7))
    frp = k.primes_above(2)[0]
    assert str(frp) == '(2, 3*_x/2 + 1/2)'

    frp = k.primes_above(3)[0]
    assert str(frp) == '(3)'

    # With alias:
    k = QQ.alg_field_from_poly(Poly(x ** 2 + 7), alias='alpha')
    frp = k.primes_above(2)[0]
    assert str(frp) == '(2, 3*alpha/2 + 1/2)'

    frp = k.primes_above(3)[0]
    assert str(frp) == '(3)'


def test_str():
    u, x, y, z = symbols("u, x:z")

    s = LineOver1DRangeSeries(cos(x), (x, -4, 3))
    assert str(s) == "cartesian line: cos(x) for x over (-4.0, 3.0)"

    d = {"return": "real"}
    s = LineOver1DRangeSeries(cos(x), (x, -4, 3), **d)
    assert str(s) == "cartesian line: re(cos(x)) for x over (-4.0, 3.0)"

    d = {"return": "imag"}
    s = LineOver1DRangeSeries(cos(x), (x, -4, 3), **d)
    assert str(s) == "cartesian line: im(cos(x)) for x over (-4.0, 3.0)"

    d = {"return": "abs"}
    s = LineOver1DRangeSeries(cos(x), (x, -4, 3), **d)
    assert str(s) == "cartesian line: abs(cos(x)) for x over (-4.0, 3.0)"

    d = {"return": "arg"}
    s = LineOver1DRangeSeries(cos(x), (x, -4, 3), **d)
    assert str(s) == "cartesian line: arg(cos(x)) for x over (-4.0, 3.0)"

    s = LineOver1DRangeSeries(cos(u * x), (x, -4, 3), params={u: 1})
    assert str(s) == "interactive cartesian line: cos(u*x) for x over (-4.0, 3.0) and parameters (u,)"

    s = LineOver1DRangeSeries(cos(u * x), (x, -u, 3*y), params={u: 1, y: 1})
    assert str(s) == "interactive cartesian line: cos(u*x) for x over (-u, 3*y) and parameters (u, y)"

    s = Parametric2DLineSeries(cos(x), sin(x), (x, -4, 3))
    assert str(s) == "parametric cartesian line: (cos(x), sin(x)) for x over (-4.0, 3.0)"

    s = Parametric2DLineSeries(cos(u * x), sin(x), (x, -4, 3), params={u: 1})
    assert str(s) == "interactive parametric cartesian line: (cos(u*x), sin(x)) for x over (-4.0, 3.0) and parameters (u,)"

    s = Parametric2DLineSeries(cos(u * x), sin(x), (x, -u, 3*y), params={u: 1, y:1})
    assert str(s) == "interactive parametric cartesian line: (cos(u*x), sin(x)) for x over (-u, 3*y) and parameters (u, y)"

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -4, 3))
    assert str(s) == "3D parametric cartesian line: (cos(x), sin(x), x) for x over (-4.0, 3.0)"

    s = Parametric3DLineSeries(cos(u*x), sin(x), x, (x, -4, 3), params={u: 1})
    assert str(s) == "interactive 3D parametric cartesian line: (cos(u*x), sin(x), x) for x over (-4.0, 3.0) and parameters (u,)"

    s = Parametric3DLineSeries(cos(u*x), sin(x), x, (x, -u, 3*y), params={u: 1, y: 1})
    assert str(s) == "interactive 3D parametric cartesian line: (cos(u*x), sin(x), x) for x over (-u, 3*y) and parameters (u, y)"

    s = SurfaceOver2DRangeSeries(cos(x * y), (x, -4, 3), (y, -2, 5))
    assert str(s) == "cartesian surface: cos(x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0)"

    s = SurfaceOver2DRangeSeries(cos(u * x * y), (x, -4, 3), (y, -2, 5), params={u: 1})
    assert str(s) == "interactive cartesian surface: cos(u*x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0) and parameters (u,)"

    s = SurfaceOver2DRangeSeries(cos(u * x * y), (x, -4*u, 3), (y, -2, 5*u), params={u: 1})
    assert str(s) == "interactive cartesian surface: cos(u*x*y) for x over (-4*u, 3.0) and y over (-2.0, 5*u) and parameters (u,)"

    s = ContourSeries(cos(x * y), (x, -4, 3), (y, -2, 5))
    assert str(s) == "contour: cos(x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0)"

    s = ContourSeries(cos(u * x * y), (x, -4, 3), (y, -2, 5), params={u: 1})
    assert str(s) == "interactive contour: cos(u*x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0) and parameters (u,)"

    s = ParametricSurfaceSeries(cos(x * y), sin(x * y), x * y,
        (x, -4, 3), (y, -2, 5))
    assert str(s) == "parametric cartesian surface: (cos(x*y), sin(x*y), x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0)"

    s = ParametricSurfaceSeries(cos(u * x * y), sin(x * y), x * y,
        (x, -4, 3), (y, -2, 5), params={u: 1})
    assert str(s) == "interactive parametric cartesian surface: (cos(u*x*y), sin(x*y), x*y) for x over (-4.0, 3.0) and y over (-2.0, 5.0) and parameters (u,)"

    s = ImplicitSeries(x < y, (x, -5, 4), (y, -3, 2))
    assert str(s) == "Implicit expression: x < y for x over (-5.0, 4.0) and y over (-3.0, 2.0)"


def test_str():
    a = intervalMembership(True, False)
    assert str(a) == 'intervalMembership(True, False)'
    assert repr(a) == 'intervalMembership(True, False)'


def test_str():
    assert str(Dimension("length")) == "Dimension(length)"
    assert str(Dimension("length", "L")) == "Dimension(length, L)"


def test_str(_test_series):
    r = _test_series.resample("h")
    assert (
        "DatetimeIndexResampler [freq=<Hour>, closed=left, "
        "label=left, convention=start, origin=start_day]" in str(r)
    )

    r = _test_series.resample("h", origin="2000-01-01")
    assert (
        "DatetimeIndexResampler [freq=<Hour>, closed=left, "
        "label=left, convention=start, origin=2000-01-01 00:00:00]" in str(r)
    )


def test_str(data, exp, transform_assert_equal):
    transform, assert_equal = transform_assert_equal
    result = to_numeric(transform(data))

    expected = transform(exp)
    assert_equal(result, expected)

