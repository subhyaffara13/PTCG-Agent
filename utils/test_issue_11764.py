
def test_issue_11764(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot_parametric(cos(x), sin(x), (x, 0, 2 * pi),
        aspect_ratio=(1,1), show=False, adaptive=adaptive, n=30)
    assert p.aspect_ratio == (1, 1)
    # Random number of segments, probably more than 100, but we want to see
    # that there are segments generated, as opposed to when the bug was present
    assert len(p[0].get_data()[0]) >= 30

