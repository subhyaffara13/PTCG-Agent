
def test_plot_and_save_6(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        filename = 'test.png'
        ###
        # Test expressions that can not be translated to np and generate complex
        # results.
        ###
        p = plot(sin(x) + I*cos(x))
        p.save(os.path.join(tmpdir, filename))

        with ignore_warnings(RuntimeWarning):
            p = plot(sqrt(sqrt(-x)))
            p.save(os.path.join(tmpdir, filename))

        p = plot(LambertW(x))
        p.save(os.path.join(tmpdir, filename))
        p = plot(sqrt(LambertW(x)))
        p.save(os.path.join(tmpdir, filename))

        #Characteristic function of a StudentT distribution with nu=10
        x1 = 5 * x**2 * exp_polar(-I*pi)/2
        m1 = meijerg(((1 / 2,), ()), ((5, 0, 1 / 2), ()), x1)
        x2 = 5*x**2 * exp_polar(I*pi)/2
        m2 = meijerg(((1/2,), ()), ((5, 0, 1/2), ()), x2)
        expr = (m1 + m2) / (48 * pi)
        with warns(
            UserWarning,
            match="The evaluation with NumPy/SciPy failed",
            test_stacklevel=False,
        ):
            p = plot(expr, (x, 1e-6, 1e-2), adaptive=adaptive, n=10)
            p.save(os.path.join(tmpdir, filename))

