
def test_issue_16572(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot(LambertW(x), show=False, adaptive=adaptive, n=30)
    # Random number of segments, probably more than 50, but we want to see
    # that there are segments generated, as opposed to when the bug was present
    assert len(p[0].get_data()[0]) >= 30

