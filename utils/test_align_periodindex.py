
def test_align_periodindex(join_type):
    rng = period_range("1/1/2000", "1/1/2010", freq="Y")
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    # TODO: assert something?
    ts.align(ts[::2], join=join_type)

