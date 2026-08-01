
def test_plot_and_save_5(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        s = Sum(1/x**y, (x, 1, oo))
        p = plot(s, (y, 2, 10), adaptive=adaptive, n=10)
        filename = 'test_advanced_inf_sum.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

        p = plot(Sum(1/x, (x, 1, y)), (y, 2, 10), show=False,
            adaptive=adaptive, n=10)
        p[0].only_integers = True
        p[0].steps = True
        filename = 'test_advanced_fin_sum.png'

        # XXX: This should be fixed in experimental_lambdify or by using
        # ordinary lambdify so that it doesn't warn. The error results from
        # passing an array of values as the integration limit.
        #
        # UserWarning: The evaluation of the expression is problematic. We are
        # trying a failback method that may still work. Please report this as a
        # bug.
        with ignore_warnings(UserWarning):
            p.save(os.path.join(tmpdir, filename))

        p._backend.close()

