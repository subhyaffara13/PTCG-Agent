
def test_issue_11865(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    k = Symbol('k', integer=True)
    f = Piecewise((-I*exp(I*pi*k)/k + I*exp(-I*pi*k)/k, Ne(k, 0)), (2*pi, True))
    p = plot(f, show=False, adaptive=adaptive, n=30)
    # Random number of segments, probably more than 100, but we want to see
    # that there are segments generated, as opposed to when the bug was present
    # and that there are no exceptions.
    assert len(p[0].get_data()[0]) >= 30

