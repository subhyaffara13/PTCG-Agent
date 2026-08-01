
def test_show_in_legend_lines():
    # verify that lines series correctly set the show_in_legend attribute
    x, u = symbols("x, u")

    s = LineOver1DRangeSeries(cos(x), (x, -2, 2), "test", show_in_legend=True)
    assert s.show_in_legend
    s = LineOver1DRangeSeries(cos(x), (x, -2, 2), "test", show_in_legend=False)
    assert not s.show_in_legend

    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 1), "test",
        show_in_legend=True)
    assert s.show_in_legend
    s = Parametric2DLineSeries(cos(x), sin(x), (x, 0, 1), "test",
        show_in_legend=False)
    assert not s.show_in_legend

    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 1), "test",
        show_in_legend=True)
    assert s.show_in_legend
    s = Parametric3DLineSeries(cos(x), sin(x), x, (x, 0, 1), "test",
        show_in_legend=False)
    assert not s.show_in_legend

