
def test_back_compatibility():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')
    p = plot(sin(x), adaptive=False, n=5)
    assert len(p[0].get_points()) == 2
    assert len(p[0].get_data()) == 2
    p = plot_parametric(cos(x), sin(x), (x, 0, 2), adaptive=False, n=5)
    assert len(p[0].get_points()) == 2
    assert len(p[0].get_data()) == 3
    p = plot3d_parametric_line(cos(x), sin(x), x, (x, 0, 2),
        adaptive=False, n=5)
    assert len(p[0].get_points()) == 3
    assert len(p[0].get_data()) == 4
    p = plot3d(cos(x**2 + y**2), (x, -pi, pi), (y, -pi, pi), n=5)
    assert len(p[0].get_meshes()) == 3
    assert len(p[0].get_data()) == 3
    p = plot_contour(cos(x**2 + y**2), (x, -pi, pi), (y, -pi, pi), n=5)
    assert len(p[0].get_meshes()) == 3
    assert len(p[0].get_data()) == 3
    p = plot3d_parametric_surface(x * cos(y), x * sin(y), x * cos(4 * y) / 2,
        (x, 0, pi), (y, 0, 2*pi), n=5)
    assert len(p[0].get_meshes()) == 3
    assert len(p[0].get_data()) == 5

