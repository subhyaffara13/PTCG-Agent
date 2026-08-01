
def test_plot3d_plot_contour_arguments():
    ### Test arguments for plot3d() and plot_contour()
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x, y = symbols("x, y")

    # single expression
    p = plot3d(x + y)
    assert isinstance(p[0], SurfaceOver2DRangeSeries)
    assert p[0].expr == x + y
    assert p[0].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[0].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[0].get_label(False) == "x + y"
    assert p[0].rendering_kw == {}

    # single expression, custom range, label and rendering kws
    p = plot3d(x + y, (x, -2, 2), "test", {"cmap": "Reds"})
    assert isinstance(p[0], SurfaceOver2DRangeSeries)
    assert p[0].expr == x + y
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -10, 10)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {"cmap": "Reds"}

    p = plot3d(x + y, (x, -2, 2), (y, -4, 4), "test")
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -4, 4)

    # multiple expressions
    p = plot3d(x + y, x * y)
    assert p[0].expr == x + y
    assert p[0].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[0].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[0].get_label(False) == "x + y"
    assert p[0].rendering_kw == {}
    assert p[1].expr == x * y
    assert p[1].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[1].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[1].get_label(False) == "x*y"
    assert p[1].rendering_kw == {}

    # multiple expressions, same custom ranges
    p = plot3d(x + y, x * y, (x, -2, 2), (y, -4, 4))
    assert p[0].expr == x + y
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -4, 4)
    assert p[0].get_label(False) == "x + y"
    assert p[0].rendering_kw == {}
    assert p[1].expr == x * y
    assert p[1].ranges[0] == (x, -2, 2)
    assert p[1].ranges[1] == (y, -4, 4)
    assert p[1].get_label(False) == "x*y"
    assert p[1].rendering_kw == {}

    # multiple expressions, custom ranges, labels and rendering kws
    p = plot3d(
        (x + y, (x, -2, 2), (y, -4, 4)),
        (x * y, (x, -3, 3), (y, -6, 6), "test", {"cmap": "Reds"}))
    assert p[0].expr == x + y
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -4, 4)
    assert p[0].get_label(False) == "x + y"
    assert p[0].rendering_kw == {}
    assert p[1].expr == x * y
    assert p[1].ranges[0] == (x, -3, 3)
    assert p[1].ranges[1] == (y, -6, 6)
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {"cmap": "Reds"}

    # single expression: lambda function
    f = lambda x, y: x + y
    p = plot3d(f)
    assert callable(p[0].expr)
    assert p[0].ranges[0][1:] == (-10, 10)
    assert p[0].ranges[1][1:] == (-10, 10)
    assert p[0].get_label(False) == ""
    assert p[0].rendering_kw == {}

    # single expression: lambda function + custom ranges + label
    p = plot3d(f, ("a", -5, 3), ("b", -2, 1), "test")
    assert callable(p[0].expr)
    assert p[0].ranges[0][1:] == (-5, 3)
    assert p[0].ranges[1][1:] == (-2, 1)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}

    # test issue 25818
    # single expression, custom range, min/max functions
    p = plot3d(Min(x, y), (x, 0, 10), (y, 0, 10))
    assert isinstance(p[0], SurfaceOver2DRangeSeries)
    assert p[0].expr == Min(x, y)
    assert p[0].ranges[0] == (x, 0, 10)
    assert p[0].ranges[1] == (y, 0, 10)
    assert p[0].get_label(False) == "Min(x, y)"
    assert p[0].rendering_kw == {}

