
def test_symbolic_plotting_ranges():
    # verify that data series can use symbolic plotting ranges
    if not np:
        skip("numpy not installed.")

    x, y, z, a, b = symbols("x, y, z, a, b")

    def do_test(s1, s2, new_params):
        d1 = s1.get_data()
        d2 = s2.get_data()
        for u, v in zip(d1, d2):
            assert np.allclose(u, v)
        s2.params = new_params
        d2 = s2.get_data()
        for u, v in zip(d1, d2):
            assert not np.allclose(u, v)

    s1 = LineOver1DRangeSeries(sin(x), (x, 0, 1), adaptive=False, n=10)
    s2 = LineOver1DRangeSeries(sin(x), (x, a, b), params={a: 0, b: 1},
        adaptive=False, n=10)
    do_test(s1, s2, {a: 0.5, b: 1.5})

    # missing a parameter
    raises(ValueError,
        lambda : LineOver1DRangeSeries(sin(x), (x, a, b), params={a: 1}, n=10))

    s1 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 1), adaptive=False, n=10)
    s2 = Parametric2DLineSeries(cos(x), sin(x), (x, a, b), params={a: 0, b: 1},
        adaptive=False, n=10)
    do_test(s1, s2, {a: 0.5, b: 1.5})

    # missing a parameter
    raises(ValueError,
        lambda : Parametric2DLineSeries(cos(x), sin(x), (x, a, b),
            params={a: 0}, adaptive=False, n=10))

    s1 = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 1),
        adaptive=False, n=10)
    s2 = Parametric3DLineSeries(cos(x), sin(x), x, (x, a, b),
        params={a: 0, b: 1}, adaptive=False, n=10)
    do_test(s1, s2, {a: 0.5, b: 1.5})

    # missing a parameter
    raises(ValueError,
        lambda : Parametric3DLineSeries(cos(x), sin(x), x, (x, a, b),
            params={a: 0}, adaptive=False, n=10))

    s1 = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -pi, pi), (y, -pi, pi),
        adaptive=False, n1=5, n2=5)
    s2 = SurfaceOver2DRangeSeries(cos(x**2 + y**2), (x, -pi * a, pi * a),
        (y, -pi * b, pi * b), params={a: 1, b: 1},
        adaptive=False, n1=5, n2=5)
    do_test(s1, s2, {a: 0.5, b: 1.5})

    # missing a parameter
    raises(ValueError,
        lambda : SurfaceOver2DRangeSeries(cos(x**2 + y**2),
        (x, -pi * a, pi * a), (y, -pi * b, pi * b), params={a: 1},
        adaptive=False, n1=5, n2=5))
    # one range symbol is included into another range's minimum or maximum val
    raises(ValueError,
        lambda : SurfaceOver2DRangeSeries(cos(x**2 + y**2),
        (x, -pi * a + y, pi * a), (y, -pi * b, pi * b), params={a: 1},
        adaptive=False, n1=5, n2=5))

    s1 = ParametricSurfaceSeries(
        cos(x - y), sin(x + y), x - y, (x, -2, 2), (y, -2, 2), n1=5, n2=5)
    s2 = ParametricSurfaceSeries(
        cos(x - y), sin(x + y), x - y, (x, -2 * a, 2), (y, -2, 2 * b),
        params={a: 1, b: 1}, n1=5, n2=5)
    do_test(s1, s2, {a: 0.5, b: 1.5})

    # missing a parameter
    raises(ValueError,
        lambda : ParametricSurfaceSeries(
        cos(x - y), sin(x + y), x - y, (x, -2 * a, 2), (y, -2, 2 * b),
        params={a: 1}, n1=5, n2=5))

