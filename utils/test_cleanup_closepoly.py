
def test_cleanup_closepoly():
    # if the first connected component of a Path ends in a CLOSEPOLY, but that
    # component contains a NaN, then Path.cleaned should ignore not just the
    # control points but also the CLOSEPOLY, since it has nowhere valid to
    # point.
    paths = [
        Path([[np.nan, np.nan], [np.nan, np.nan]],
             [Path.MOVETO, Path.CLOSEPOLY]),
        # we trigger a different path in the C++ code if we don't pass any
        # codes explicitly, so we must also make sure that this works
        Path([[np.nan, np.nan], [np.nan, np.nan]]),
        # we should also make sure that this cleanup works if there's some
        # multi-vertex curves
        Path([[np.nan, np.nan], [np.nan, np.nan], [np.nan, np.nan],
              [np.nan, np.nan]],
             [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY])
    ]
    for p in paths:
        cleaned = p.cleaned(remove_nans=True)
        assert len(cleaned) == 1
        assert cleaned.codes[0] == Path.STOP

