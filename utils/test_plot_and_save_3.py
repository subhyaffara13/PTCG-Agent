
def test_plot_and_save_3(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        ###
        # Examples from the 'colors' notebook
        ###

        p = plot(sin(x), adaptive=adaptive, n=10)
        p[0].line_color = lambda a: a
        filename = 'test_colors_line_arity1.png'
        p.save(os.path.join(tmpdir, filename))

        p[0].line_color = lambda a, b: b
        filename = 'test_colors_line_arity2.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot(x*sin(x), x*cos(x), (x, 0, 10), adaptive=adaptive, n=10)
        p[0].line_color = lambda a: a
        filename = 'test_colors_param_line_arity1.png'
        p.save(os.path.join(tmpdir, filename))

        p[0].line_color = lambda a, b: a
        filename = 'test_colors_param_line_arity1.png'
        p.save(os.path.join(tmpdir, filename))

        p[0].line_color = lambda a, b: b
        filename = 'test_colors_param_line_arity2b.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot3d_parametric_line(
            sin(x) + 0.1*sin(x)*cos(7*x),
            cos(x) + 0.1*cos(x)*cos(7*x),
            0.1*sin(7*x),
            (x, 0, 2*pi), adaptive=adaptive, n=10)
        p[0].line_color = lambdify_(x, sin(4*x))
        filename = 'test_colors_3d_line_arity1.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].line_color = lambda a, b: b
        filename = 'test_colors_3d_line_arity2.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].line_color = lambda a, b, c: c
        filename = 'test_colors_3d_line_arity3.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot3d(sin(x)*y, (x, 0, 6*pi), (y, -5, 5), adaptive=adaptive, n=10)
        p[0].surface_color = lambda a: a
        filename = 'test_colors_surface_arity1.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].surface_color = lambda a, b: b
        filename = 'test_colors_surface_arity2.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].surface_color = lambda a, b, c: c
        filename = 'test_colors_surface_arity3a.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].surface_color = lambdify_((x, y, z), sqrt((x - 3*pi)**2 + y**2))
        filename = 'test_colors_surface_arity3b.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot3d_parametric_surface(x * cos(4 * y), x * sin(4 * y), y,
                (x, -1, 1), (y, -1, 1), adaptive=adaptive, n=10)
        p[0].surface_color = lambda a: a
        filename = 'test_colors_param_surf_arity1.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].surface_color = lambda a, b: a*b
        filename = 'test_colors_param_surf_arity2.png'
        p.save(os.path.join(tmpdir, filename))
        p[0].surface_color = lambdify_((x, y, z), sqrt(x**2 + y**2 + z**2))
        filename = 'test_colors_param_surf_arity3.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

