
def test_is_point_is_filled():
    # verify that `is_point` and `is_filled` are attributes and that they
    # they receive the correct values
    if not np:
        skip("numpy not installed.")

    x, u = symbols("x, u")

    s = LineOver1DRangeSeries(cos(x), (x, -5, 5), "",
        is_point=False, is_filled=True)
    assert (not s.is_point) and s.is_filled
    s = LineOver1DRangeSeries(cos(x), (x, -5, 5), "",
        is_point=True, is_filled=False)
    assert s.is_point and (not s.is_filled)

    s = List2DSeries([0, 1, 2], [3, 4, 5],
        is_point=False, is_filled=True)
    assert (not s.is_point) and s.is_filled
    s = List2DSeries([0, 1, 2], [3, 4, 5],
        is_point=True, is_filled=False)
    assert s.is_point and (not s.is_filled)

    s = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5),
        is_point=False, is_filled=True)
    assert (not s.is_point) and s.is_filled
    s = Parametric2DLineSeries(cos(x), sin(x), (x, -5, 5),
        is_point=True, is_filled=False)
    assert s.is_point and (not s.is_filled)

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5),
        is_point=False, is_filled=True)
    assert (not s.is_point) and s.is_filled
    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, -5, 5),
        is_point=True, is_filled=False)
    assert s.is_point and (not s.is_filled)

