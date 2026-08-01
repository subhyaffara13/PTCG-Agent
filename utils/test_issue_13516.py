
def test_issue_13516(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')

    pm = plot(sin(x), backend="matplotlib", show=False, adaptive=adaptive, n=30)
    assert pm.backend == MatplotlibBackend
    assert len(pm[0].get_data()[0]) >= 30

    pt = plot(sin(x), backend="text", show=False, adaptive=adaptive, n=30)
    assert pt.backend == TextBackend
    assert len(pt[0].get_data()[0]) >= 30

    pd = plot(sin(x), backend="default", show=False, adaptive=adaptive, n=30)
    assert pd.backend == MatplotlibBackend
    assert len(pd[0].get_data()[0]) >= 30

    p = plot(sin(x), show=False, adaptive=adaptive, n=30)
    assert p.backend == MatplotlibBackend
    assert len(p[0].get_data()[0]) >= 30

