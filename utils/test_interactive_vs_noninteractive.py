
def test_interactive_vs_noninteractive():
    # verify that if a *Series class receives a `params` dictionary, it sets
    # is_interactive=True
    x, y, z, u, v = symbols("x, y, z, u, v")

    s = LineOver1DRangeSeries(cos(x), (x, -5, 5))
    assert not s.is_interactive
    s = LineOver1DRangeSeries(u * cos(x), (x, -5, 5), params={u: 1})
    assert s.is_interactive

    s = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5))
    assert not s.is_interactive
    s = Parametric2DLineSeries(u * cos(x), u * sin(x), (x, -5, 5),
        params={u: 1})
    assert s.is_interactive

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5))
    assert not s.is_interactive
    s = Parametric3DLineSeries(u * cos(x), u * sin(x), x, (x, -5, 5),
        params={u: 1})
    assert s.is_interactive

    s = SurfaceOver2DRangeSeries(cos(x * y), (x, -5, 5), (y, -5, 5))
    assert not s.is_interactive
    s = SurfaceOver2DRangeSeries(u * cos(x * y), (x, -5, 5), (y, -5, 5),
        params={u: 1})
    assert s.is_interactive

    s = ContourSeries(cos(x * y), (x, -5, 5), (y, -5, 5))
    assert not s.is_interactive
    s = ContourSeries(u * cos(x * y), (x, -5, 5), (y, -5, 5),
        params={u: 1})
    assert s.is_interactive

    s = ParametricSurfaceSeries(u * cos(v), v * sin(u), u + v,
        (u, -5, 5), (v, -5, 5))
    assert not s.is_interactive
    s = ParametricSurfaceSeries(u * cos(v * x), v * sin(u), u + v,
        (u, -5, 5), (v, -5, 5), params={x: 1})
    assert s.is_interactive

