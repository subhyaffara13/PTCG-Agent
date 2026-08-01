
def test_plot3d_parametric_surface_arguments():
    ### Test arguments for plot3d_parametric_surface()
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x, y = symbols("x, y")

    # single parametric expression
    p = plot3d_parametric_surface(x + y, cos(x + y), sin(x + y))
    assert isinstance(p[0], ParametricSurfaceSeries)
    assert p[0].expr == (x + y, cos(x + y), sin(x + y))
    assert p[0].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[0].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[0].get_label(False) == "(x + y, cos(x + y), sin(x + y))"
    assert p[0].rendering_kw == {}

    # single parametric expression, custom ranges, labels and rendering kws
    p = plot3d_parametric_surface(x + y, cos(x + y), sin(x + y),
        (x, -2, 2), (y, -4, 4), "test", {"cmap": "Reds"})
    assert isinstance(p[0], ParametricSurfaceSeries)
    assert p[0].expr == (x + y, cos(x + y), sin(x + y))
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -4, 4)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {"cmap": "Reds"}

    # multiple parametric expressions
    p = plot3d_parametric_surface(
        (x + y, cos(x + y), sin(x + y)),
        (x - y, cos(x - y), sin(x - y), "test"))
    assert p[0].expr == (x + y, cos(x + y), sin(x + y))
    assert p[0].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[0].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[0].get_label(False) == "(x + y, cos(x + y), sin(x + y))"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x - y, cos(x - y), sin(x - y))
    assert p[1].ranges[0] == (x, -10, 10) or (y, -10, 10)
    assert p[1].ranges[1] == (x, -10, 10) or (y, -10, 10)
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {}

    # multiple parametric expressions, custom ranges and labels
    p = plot3d_parametric_surface(
        (x + y, cos(x + y), sin(x + y), (x, -2, 2), "test"),
        (x - y, cos(x - y), sin(x - y), (x, -3, 3), (y, -4, 4),
            "test2", {"cmap": "Reds"}))
    assert p[0].expr == (x + y, cos(x + y), sin(x + y))
    assert p[0].ranges[0] == (x, -2, 2)
    assert p[0].ranges[1] == (y, -10, 10)
    assert p[0].get_label(False) == "test"
    assert p[0].rendering_kw == {}
    assert p[1].expr == (x - y, cos(x - y), sin(x - y))
    assert p[1].ranges[0] == (x, -3, 3)
    assert p[1].ranges[1] == (y, -4, 4)
    assert p[1].get_label(False) == "test2"
    assert p[1].rendering_kw == {"cmap": "Reds"}

    # lambda functions instead of symbolic expressions for a single 3D
    # parametric surface
    p = plot3d_parametric_surface(
        lambda u, v: u, lambda u, v: v, lambda u, v: u + v,
        ("u", 0, 2), ("v", -3, 4))
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (-0, 2)
    assert p[0].ranges[1][1:] == (-3, 4)
    assert p[0].get_label(False) == ""
    assert p[0].rendering_kw == {}

    # lambda functions instead of symbolic expressions for multiple 3D
    # parametric surfaces
    p = plot3d_parametric_surface(
        (lambda u, v: u, lambda u, v: v, lambda u, v: u + v,
        ("u", 0, 2), ("v", -3, 4)),
        (lambda u, v: v, lambda u, v: u, lambda u, v: u - v,
        ("u", -2, 3), ("v", -4, 5), "test"))
    assert all(callable(t) for t in p[0].expr)
    assert p[0].ranges[0][1:] == (0, 2)
    assert p[0].ranges[1][1:] == (-3, 4)
    assert p[0].get_label(False) == ""
    assert p[0].rendering_kw == {}
    assert all(callable(t) for t in p[1].expr)
    assert p[1].ranges[0][1:] == (-2, 3)
    assert p[1].ranges[1][1:] == (-4, 5)
    assert p[1].get_label(False) == "test"
    assert p[1].rendering_kw == {}

