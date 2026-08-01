
def test_plot_size(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')

    p1 = plot(sin(x), backend="matplotlib", size=(8, 4),
        adaptive=adaptive, n=10)
    s1 = p1._backend.fig.get_size_inches()
    assert (s1[0] == 8) and (s1[1] == 4)
    p2 = plot(sin(x), backend="matplotlib", size=(5, 10),
        adaptive=adaptive, n=10)
    s2 = p2._backend.fig.get_size_inches()
    assert (s2[0] == 5) and (s2[1] == 10)
    p3 = PlotGrid(2, 1, p1, p2, size=(6, 2),
        adaptive=adaptive, n=10)
    s3 = p3._backend.fig.get_size_inches()
    assert (s3[0] == 6) and (s3[1] == 2)

    with raises(ValueError):
        plot(sin(x), backend="matplotlib", size=(-1, 3))

