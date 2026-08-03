import os

def test_plotgrid_and_save(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        p1 = plot(x, adaptive=adaptive, n=10)
        p2 = plot_parametric((sin(x), cos(x)), (x, sin(x)), show=False,
            adaptive=adaptive, n=10)
        p3 = plot_parametric(
            cos(x), sin(x), adaptive=adaptive, n=10, show=False)
        p4 = plot3d_parametric_line(sin(x), cos(x), x, show=False,
            adaptive=adaptive, n=10)
        # symmetric grid
        p = PlotGrid(2, 2, p1, p2, p3, p4)
        filename = 'test_grid1.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # grid size greater than the number of subplots
        p = PlotGrid(3, 4, p1, p2, p3, p4)
        filename = 'test_grid2.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p5 = plot(cos(x),(x, -pi, pi), show=False, adaptive=adaptive, n=10)
        p5[0].line_color = lambda a: a
        p6 = plot(Piecewise((1, x > 0), (0, True)), (x, -1, 1), show=False,
            adaptive=adaptive, n=10)
        p7 = plot_contour(
            (x**2 + y**2, (x, -5, 5), (y, -5, 5)),
            (x**3 + y**3, (x, -3, 3), (y, -3, 3)), show=False,
            adaptive=adaptive, n=10)
        # unsymmetric grid (subplots in one line)
        p = PlotGrid(1, 3, p5, p6, p7)
        filename = 'test_grid3.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

