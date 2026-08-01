
def test_plot3d_parametric_line_arguments():
    ### Test arguments for plot3d_parametric_line()
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x, y = symbols("x, y")

    # single parametric expression
    p = plot3d_parametric_line(x + 1, x, sin(x))
    assert isinstance(p[0], Parametric3DLineSeries)
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}

    # single parametric expression with custom range, label and rendering kws
    p = plot3d_parametric_line(x + 1, x, sin(x), (x, -2, 2),
        "test", {"cmap": "Reds"})
    assert isinstance(p[0], Parametric3DLineSeries)
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {"cmap": "Reds"}

    p = plot3d_parametric_line((x + 1, x, sin(x)), (x, -2, 2), "test")
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -2, 2)]
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}

    # multiple parametric expression same symbol
    p = plot3d_parametric_line(
        (x + 1, x, sin(x)), (x ** 2, 1, cos(x), {"cmap": "Reds"}))
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x ** 2, 1, cos(x))
    assert p[1].ranges == [(x, -10, 10)]
    assert p[1].get_label(False) == "x"
    assert p[1].rendering_kw == {"cmap": "Reds"}

    # multiple parametric expression different symbols
    p = plot3d_parametric_line((x + 1, x, sin(x)), (y ** 2, 1, cos(y)))
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (y ** 2, 1, cos(y))
    assert p[1].ranges == [(y, -10, 10)]
    assert p[1].get_label(False) == "y"
    assert p[1].rendering_kw == {}

    # multiple parametric expression, custom ranges and labels
    p = plot3d_parametric_line(
        (x + 1, x, sin(x)),
        (x ** 2, 1, cos(x), (x, -2, 2), "test", {"cmap": "Reds"}))
    assert p[0].expr == (x + 1, x, sin(x))
    assert p[0].ranges == [(x, -10, 10)]
    assert p[0].get_label(False) == "x"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x ** 2, 1, cos(x))
    assert p[1].ranges == [(x, -2, 2)]
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {"cmap": "Reds"}

    # single argument: lambda function
    fx = lambda t: t
    fy = lambda t: 2 * t
    fz = lambda t: 3 * t
    p = plot3d_parametric_line(fx, fy, fz)
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (-10, 10)
    assert "Dummy" in p[0].get_label(False)
    assert p[0].rendering_kw == {}

    # single argument: lambda function + custom range + label
    p = plot3d_parametric_line(fx, fy, fz, ("t", 0, 2), "test")
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (0, 2)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}

