
def test_number_discretization_points():
    # verify that the different ways to set the number of discretization
    # points are consistent with each other.
    if not np:
        skip("numpy not installed.")

    x, y, z = symbols("x:z")

    for pt in [LineOver1DRangeSeries, Parametric2DLineSeries,
        Parametric3DLineSeries]:
        kw1 = _set_discretization_points({"n": 10}, pt)
        kw2 = _set_discretization_points({"n": [10, 20, 30]}, pt)
        kw3 = _set_discretization_points({"n1": 10}, pt)
        assert all(("n1" in kw) and kw["n1"] == 10 for kw in [kw1, kw2, kw3])

    for pt in [SurfaceOver2DRangeSeries, ContourSeries, ParametricSurfaceSeries,
        ImplicitSeries]:
        kw1 = _set_discretization_points({"n": 10}, pt)
        kw2 = _set_discretization_points({"n": [10, 20, 30]}, pt)
        kw3 = _set_discretization_points({"n1": 10, "n2": 20}, pt)
        assert kw1["n1"] == kw1["n2"] == 10
        assert all((kw["n1"] == 10) and (kw["n2"] == 20) for kw in [kw2, kw3])

    # verify that line-related series can deal with large float number of
    # discretization points
    LineOver1DRangeSeries(cos(x), (x, -5, 5), adaptive=False, n=1e04).get_data()

