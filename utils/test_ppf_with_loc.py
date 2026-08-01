
def test_ppf_with_loc(dist, args):
    try:
        distfn = getattr(stats, dist)
    except TypeError:
        distfn = dist
    #check with a negative, no and positive relocation.
    rng = np.random.default_rng(5108587887)

    re_locs = [rng.integers(-10, -1), 0, rng.integers(1, 10)]
    _a, _b = distfn.support(*args)
    for loc in re_locs:
        npt.assert_array_equal(
            [_a-1+loc, _b+loc],
            [distfn.ppf(0.0, *args, loc=loc), distfn.ppf(1.0, *args, loc=loc)]
            )

