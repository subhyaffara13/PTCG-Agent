
def test_custom_coloring():
    x = Symbol('x')
    y = Symbol('y')
    plot(cos(x), line_color=lambda a: a)
    plot(cos(x), line_color=1)
    plot(cos(x), line_color="r")
    plot_parametric(cos(x), sin(x), line_color=lambda a: a)
    plot_parametric(cos(x), sin(x), line_color=1)
    plot_parametric(cos(x), sin(x), line_color="r")
    plot3d_parametric_line(cos(x), sin(x), x, line_color=lambda a: a)
    plot3d_parametric_line(cos(x), sin(x), x, line_color=1)
    plot3d_parametric_line(cos(x), sin(x), x, line_color="r")
    plot3d_parametric_surface(cos(x + y), sin(x - y), x - y,
            (x, -5, 5), (y, -5, 5),
            surface_color=lambda a, b: a**2 + b**2)
    plot3d_parametric_surface(cos(x + y), sin(x - y), x - y,
            (x, -5, 5), (y, -5, 5),
            surface_color=1)
    plot3d_parametric_surface(cos(x + y), sin(x - y), x - y,
            (x, -5, 5), (y, -5, 5),
            surface_color="r")
    plot3d(x*y, (x, -5, 5), (y, -5, 5),
            surface_color=lambda a, b: a**2 + b**2)
    plot3d(x*y, (x, -5, 5), (y, -5, 5), surface_color=1)
    plot3d(x*y, (x, -5, 5), (y, -5, 5), surface_color="r")

