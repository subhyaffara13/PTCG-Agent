
def test_issue_11461():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p = plot(real_root((log(x/(x-2))), 3), show=False, adaptive=True)
    with warns(
        RuntimeWarning,
        match="invalid value encountered in",
        test_stacklevel=False,
    ):
        # Random number of segments, probably more than 100, but we want to see
        # that there are segments generated, as opposed to when the bug was present
        # and that there are no exceptions.
        assert len(p[0].get_data()[0]) >= 30

