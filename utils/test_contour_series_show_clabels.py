
def test_contour_series_show_clabels():
    # verify that a contour series has the abiliy to set the visibility of
    # labels to contour lines

    x, y = symbols("x, y")
    s = ContourSeries(cos(x*y), (x, -2, 2), (y, -2, 2))
    assert s.show_clabels

    s = ContourSeries(cos(x*y), (x, -2, 2), (y, -2, 2), clabels=True)
    assert s.show_clabels

    s = ContourSeries(cos(x*y), (x, -2, 2), (y, -2, 2), clabels=False)
    assert not s.show_clabels

