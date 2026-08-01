
def test_adaptive():
    # verify that adaptive-related keywords produces the expected results
    if not np:
        skip("numpy not installed.")

    x, y = symbols("x, y")

    s1 = LineOver1DRangeSeries(sin(x), (x, -10, 10), "", adaptive=True,
        depth=2)
    x1, _ = s1.get_data()
    s2 = LineOver1DRangeSeries(sin(x), (x, -10, 10), "", adaptive=True,
        depth=5)
    x2, _ = s2.get_data()
    s3 = LineOver1DRangeSeries(sin(x), (x, -10, 10), "", adaptive=True)
    x3, _ = s3.get_data()
    assert len(x1) < len(x2) < len(x3)

    s1 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=True, depth=2)
    x1, _, _, = s1.get_data()
    s2 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=True, depth=5)
    x2, _, _ = s2.get_data()
    s3 = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 2*pi),
        adaptive=True)
    x3, _, _ = s3.get_data()
    assert len(x1) < len(x2) < len(x3)

