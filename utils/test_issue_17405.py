
def test_issue_17405(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    f = x**0.3 - 10*x**3 + x**2
    p = plot(f, (x, -10, 10), adaptive=adaptive, n=30, show=False)
    # Random number of segments, probably more than 100, but we want to see
    # that there are segments generated, as opposed to when the bug was present

    # RuntimeWarning: invalid value encountered in double_scalars
    with ignore_warnings(RuntimeWarning):
        assert len(p[0].get_data()[0]) >= 30

