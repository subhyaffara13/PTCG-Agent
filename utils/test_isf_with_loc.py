
def test_isf_with_loc(dist, args):
    try:
        distfn = getattr(stats, dist)
    except TypeError:
        distfn = dist
    # check with a negative, no and positive relocation.
    rng = np.random.default_rng(4030503535)
    re_locs = [rng.integers(-10, -1), 0, rng.integers(1, 10)]
    _a, _b = distfn.support(*args)
    for loc in re_locs:
        expected = _b + loc, _a - 1 + loc
        res = distfn.isf(0., *args, loc=loc), distfn.isf(1., *args, loc=loc)
        npt.assert_array_equal(expected, res)
    # test broadcasting behaviour
    re_locs = [rng.integers(-10, -1, size=(5, 3)),
               np.zeros((5, 3)),
               rng.integers(1, 10, size=(5, 3))]
    _a, _b = distfn.support(*args)
    for loc in re_locs:
        expected = _b + loc, _a - 1 + loc
        res = distfn.isf(0., *args, loc=loc), distfn.isf(1., *args, loc=loc)
        npt.assert_array_equal(expected, res)

