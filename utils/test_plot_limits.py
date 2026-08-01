
def test_plot_limits(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot(x, x**2, (x, -10, 10), adaptive=adaptive, n=10)
    backend = p._backend

    xmin, xmax = backend.ax.get_xlim()
    assert abs(xmin + 10) < 2
    assert abs(xmax - 10) < 2
    ymin, ymax = backend.ax.get_ylim()
    assert abs(ymin + 10) < 10
    assert abs(ymax - 100) < 10

