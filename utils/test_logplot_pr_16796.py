
def test_logplot_PR_16796(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot(x, (x, .001, 100), adaptive=adaptive, n=30,
        xscale='log', show=False)
    # Random number of segments, probably more than 100, but we want to see
    # that there are segments generated, as opposed to when the bug was present
    assert len(p[0].get_data()[0]) >= 30
    assert p[0].end == 100.0
    assert p[0].start == .001

