
def test_is_filled_2d():
    # verify that the is_filled attribute is exposed by the following series
    x, y = symbols("x, y")

    expr = cos(x**2 + y**2)
    ranges = (x, -2, 2), (y, -2, 2)

    s = ContourSeries(expr, *ranges)
    assert s.is_filled
    s = ContourSeries(expr, *ranges, is_filled=True)
    assert s.is_filled
    s = ContourSeries(expr, *ranges, is_filled=False)
    assert not s.is_filled

