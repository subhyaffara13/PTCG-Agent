import os

def test_plot_and_save_4(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    y = Symbol('y')

    ###
    # Examples from the 'advanced' notebook
    ###

    with TemporaryDirectory(prefix='sympy_') as tmpdir:
        i = Integral(log((sin(x)**2 + 1)*sqrt(x**2 + 1)), (x, 0, y))
        p = plot(i, (y, 1, 5), adaptive=adaptive, n=10, force_real_eval=True)
        filename = 'test_advanced_integral.png'
        p.save(os.path.join(tmpdir, filename))
        p._backend.close()

