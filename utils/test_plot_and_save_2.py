import os

def test_plot_and_save_2(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        #parametric 2d plots.
        #Single plot with default range.
        p = plot_parametric(sin(x), cos(x), adaptive=adaptive, n=10)
        filename = 'test_parametric.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #Single plot with range.
        p = plot_parametric(
            sin(x), cos(x), (x, -5, 5), legend=True, label='parametric_plot',
            adaptive=adaptive, n=10)
        filename = 'test_parametric_range.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #Multiple plots with same range.
        p = plot_parametric((sin(x), cos(x)), (x, sin(x)),
            adaptive=adaptive, n=10)
        filename = 'test_parametric_multiple.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #Multiple plots with different ranges.
        p = plot_parametric(
            (sin(x), cos(x), (x, -3, 3)), (x, sin(x), (x, -5, 5)),
            adaptive=adaptive, n=10)
        filename = 'test_parametric_multiple_ranges.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #depth of recursion specified.
        p = plot_parametric(x, sin(x), depth=13,
            adaptive=adaptive, n=10)
        filename = 'test_recursion_depth.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #No adaptive sampling.
        p = plot_parametric(cos(x), sin(x), adaptive=False, n=500)
        filename = 'test_adaptive.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        #3d parametric plots
        p = plot3d_parametric_line(
            sin(x), cos(x), x, legend=True, label='3d_parametric_plot',
            adaptive=adaptive, n=10)
        filename = 'test_3d_line.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot3d_parametric_line(
            (sin(x), cos(x), x, (x, -5, 5)), (cos(x), sin(x), x, (x, -3, 3)),
            adaptive=adaptive, n=10)
        filename = 'test_3d_line_multiple.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot3d_parametric_line(sin(x), cos(x), x, n=30,
            adaptive=adaptive)
        filename = 'test_3d_line_points.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # 3d surface single plot.
        p = plot3d(x * y, adaptive=adaptive, n=10)
        filename = 'test_surface.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Multiple 3D plots with same range.
        p = plot3d(-x * y, x * y, (x, -5, 5), adaptive=adaptive, n=10)
        filename = 'test_surface_multiple.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Multiple 3D plots with different ranges.
        p = plot3d(
            (x * y, (x, -3, 3), (y, -3, 3)), (-x * y, (x, -3, 3), (y, -3, 3)),
            adaptive=adaptive, n=10)
        filename = 'test_surface_multiple_ranges.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Single Parametric 3D plot
        p = plot3d_parametric_surface(sin(x + y), cos(x - y), x - y,
            adaptive=adaptive, n=10)
        filename = 'test_parametric_surface.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Multiple Parametric 3D plots.
        p = plot3d_parametric_surface(
            (x*sin(z), x*cos(z), z, (x, -5, 5), (z, -5, 5)),
            (sin(x + y), cos(x - y), x - y, (x, -5, 5), (y, -5, 5)),
            adaptive=adaptive, n=10)
        filename = 'test_parametric_surface.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Single Contour plot.
        p = plot_contour(sin(x)*sin(y), (x, -5, 5), (y, -5, 5),
            adaptive=adaptive, n=10)
        filename = 'test_contour_plot.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Multiple Contour plots with same range.
        p = plot_contour(x**2 + y**2, x**3 + y**3, (x, -5, 5), (y, -5, 5),
            adaptive=adaptive, n=10)
        filename = 'test_contour_plot.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        # Multiple Contour plots with different range.
        p = plot_contour(
            (x**2 + y**2, (x, -5, 5), (y, -5, 5)),
            (x**3 + y**3, (x, -3, 3), (y, -3, 3)),
            adaptive=adaptive, n=10)
        filename = 'test_contour_plot.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

