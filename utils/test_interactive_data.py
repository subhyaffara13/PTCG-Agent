import re

def test_interactive_data():
    # verify that InteractiveSeries produces the same numerical data as their
    # corresponding non-interactive series.
    if not np:
        skip("numpy not installed.")

    u, x, y, z = symbols("u, x:z")

    def do_test(data1, data2):
        assert len(data1) == len(data2)
        for d1, d2 in zip(data1, data2):
            assert np.allclose(d1, d2)

    s1 = LineOver1DRangeSeries(u * cos(x), (x, -5, 5), params={u: 1}, n=50)
    s2 = LineOver1DRangeSeries(cos(x), (x, -5, 5), adaptive=False, n=50)
    do_test(s1.get_data(), s2.get_data())

    s1 = Parametric2DLineSeries(
        u * cos(x), u * sin(x), (x, -5, 5), params={u: 1}, n=50)
    s2 = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5),
        adaptive=False, n=50)
    do_test(s1.get_data(), s2.get_data())

    s1 = Parametric3DLineSeries(
        u * cos(x), u * sin(x), u * x, (x, -5, 5),
        params={u: 1}, n=50)
    s2 = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5),
        adaptive=False, n=50)
    do_test(s1.get_data(), s2.get_data())

    s1 = SurfaceOver2DRangeSeries(
        u * cos(x ** 2 + y ** 2), (x, -3, 3), (y, -3, 3),
        params={u: 1}, n1=50, n2=50,)
    s2 = SurfaceOver2DRangeSeries(
        cos(x ** 2 + y ** 2), (x, -3, 3), (y, -3, 3),
        adaptive=False, n1=50, n2=50)
    do_test(s1.get_data(), s2.get_data())

    s1 = ParametricSurfaceSeries(
        u * cos(x + y), sin(x + y), x - y, (x, -3, 3), (y, -3, 3),
        params={u: 1}, n1=50, n2=50,)
    s2 = ParametricSurfaceSeries(
        cos(x + y), sin(x + y), x - y, (x, -3, 3), (y, -3, 3),
        adaptive=False, n1=50, n2=50,)
    do_test(s1.get_data(), s2.get_data())

    # real part of a complex function evaluated over a real line with numpy
    expr = re((z ** 2 + 1) / (z ** 2 - 1))
    s1 = LineOver1DRangeSeries(u * expr, (z, -3, 3), adaptive=False, n=50,
        modules=None, params={u: 1})
    s2 = LineOver1DRangeSeries(expr, (z, -3, 3), adaptive=False, n=50,
        modules=None)
    do_test(s1.get_data(), s2.get_data())

    # real part of a complex function evaluated over a real line with mpmath
    expr = re((z ** 2 + 1) / (z ** 2 - 1))
    s1 = LineOver1DRangeSeries(u * expr, (z, -3, 3), n=50, modules="mpmath",
        params={u: 1})
    s2 = LineOver1DRangeSeries(expr, (z, -3, 3),
        adaptive=False, n=50, modules="mpmath")
    do_test(s1.get_data(), s2.get_data())

