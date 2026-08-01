
def test_plot_parametric_arguments():
    ### Test arguments for plot_parametric()
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x, y = symbols("x, y")

    # single parametric expression
    p = plot_parametric(x + 1, x)
    assert isinstance(p[0], Parametric2DLineSeries)
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}

    # single parametric expression with custom range, label and rendering kws
    p = plot_parametric(x + 1, x, (x, -2, 2), "test",
        {"cmap": "Reds"})
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {"cmap": "Reds"}

    p = plot_parametric((x + 1, x), (x, -2, 2), "test")
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}

    # multiple parametric expressions same symbol
    p = plot_parametric((x + 1, x), (x ** 2, x + 1))
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x ** 2, x + 1)
    assert p[1].ranges == [(x, -10, 10)]
    assert p[1].get_label(False) == "x"
    assert p[1].rendering_kw == {}

    # multiple parametric expressions different symbols
    p = plot_parametric((x + 1, x), (y ** 2, y + 1, "test"))
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (y ** 2, y + 1)
    assert p[1].ranges == [(y, -10, 10)]
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {}

    # multiple parametric expressions same range
    p = plot_parametric((x + 1, x), (x ** 2, x + 1), (x, -2, 2))
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x ** 2, x + 1)
    assert p[1].ranges == [(x, -2, 2)]
    assert p[1].get_label(False) == "x"
    assert p[1].rendering_kw == {}

    # multiple parametric expressions, custom ranges and labels
    p = plot_parametric(
        (x + 1, x, (x, -2, 2), "test1"),
        (x ** 2, x + 1, (x, -3, 3), "test2", {"cmap": "Reds"}))
    assert p[0].expr == (x + 1, x)
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "test1"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x ** 2, x + 1)
    assert p[1].ranges == [(x, -3, 3)]
    assert p[1].get_label(False) == "test2"
    assert p[1].rendering_kw == {"cmap": "Reds"}

    # single argument: lambda function
    fx = lambda t: t
    fy = lambda t: 2 * t
    p = plot_parametric(fx, fy)
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (-10, 10)
    assert "Dummy" in p[0].get_label(False)
    assert p[0].rendering_kw == {}

    # single argument: lambda function + custom range + label
    p = plot_parametric(fx, fy, ("t", 0, 2), "test")
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (0, 2)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}

