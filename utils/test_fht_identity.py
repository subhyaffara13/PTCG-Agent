
def test_fht_identity(n, bias, offset, optimal, xp):
    rng = np.random.RandomState(3491349965)

    a = xp.asarray(rng.standard_normal(n))
    dln = rng.uniform(-1, 1)
    mu = rng.uniform(-2, 2)

    if optimal:
        offset = fhtoffset(dln, mu, initial=offset, bias=bias)
        # offset is a np.float64, which array-api-strict disallows
        # even if it's technically a subclass of float
        offset = float(offset)

    A = fht(a, dln, mu, offset=offset, bias=bias)
    a_ = ifht(A, dln, mu, offset=offset, bias=bias)

    xp_assert_close(a_, a, rtol=1.5e-7)

