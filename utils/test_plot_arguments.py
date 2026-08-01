
def test_plot_arguments():
    ### Test arguments for plot()
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x, y = symbols("x, y")

    # single expressions
    p = plot(x + 1)
    assert isinstance(p[0], LineOver1DRangeSeries)
    assert p[0].expr == x + 1
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x + 1"
    assert p[0].rendering_kw == {}

    # single expressions custom label
    p = plot(x + 1, "label")
    assert isinstance(p[0], LineOver1DRangeSeries)
    assert p[0].expr == x + 1
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "label"
    assert p[0].rendering_kw == {}

    # single expressions with range
    p = plot(x + 1, (x, -2, 2))
    assert p[0].ranges == [(x, -2, 2)]

    # single expressions with range, label and rendering-kw dictionary
    p = plot(x + 1, (x, -2, 2), "test", {"color": "r"})
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {"color": "r"}

    # multiple expressions
    p = plot(x + 1, x**2)
    assert isinstance(p[0], LineOver1DRangeSeries)
    assert p[0].expr == x + 1
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x + 1"
    assert p[0].rendering_kw == {}
    assert isinstance(p[1], LineOver1DRangeSeries)
    assert p[1].expr == x**2
    assert p[1].ranges == [(x, -10, 10)]
    assert p[1].get_label(False) == "x**2"
    assert p[1].rendering_kw == {}

    # multiple expressions over the same range
    p = plot(x + 1, x**2, (x, 0, 5))
    assert p[0].ranges == [(x, 0, 5)]
    assert p[1].ranges == [(x, 0, 5)]

    # multiple expressions over the same range with the same rendering kws
    p = plot(x + 1, x**2, (x, 0, 5), {"color": "r"})
    assert p[0].ranges == [(x, 0, 5)]
    assert p[1].ranges == [(x, 0, 5)]
    assert p[0].rendering_kw == {"color": "r"}
    assert p[1].rendering_kw == {"color": "r"}

    # multiple expressions with different ranges, labels and rendering kws
    p = plot(
        (x + 1, (x, 0, 5)),
        (x**2, (x, -2, 2), "test", {"color": "r"}))
    assert isinstance(p[0], LineOver1DRangeSeries)
    assert p[0].expr == x + 1
    assert p[0].ranges == [(x, 0, 5)]
    assert p[0].get_label(False) == "x + 1"
    assert p[0].rendering_kw == {}
    assert isinstance(p[1], LineOver1DRangeSeries)
    assert p[1].expr == x**2
    assert p[1].ranges == [(x, -2, 2)]
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {"color": "r"}

    # single argument: lambda function
    f = lambda t: t
    p = plot(lambda t: t)
    assert isinstance(p[0], LineOver1DRangeSeries)
    assert callable(p[0].expr)
    assert p[0].ranges[0][1:] == (-10, 10)
    assert p[0].get_label(False) == ""
    assert p[0].rendering_kw == {}

    # single argument: lambda function + custom range and label
    p = plot(f, ("t", -5, 6), "test")
    assert p[0].ranges[0][1:] == (-5, 6)
    assert p[0].get_label(False) == "test"

