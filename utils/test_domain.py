
def test_domain():
    # only a basic check that the domain argument is passed to the
    # UNU.RAN generators
    rng = FastGeneratorInversion(stats.norm(), domain=(-1, 1))
    r = rng.rvs(size=100)
    assert -1 <= r.min() < r.max() <= 1

    # if loc and scale are used, new domain is loc + scale*domain
    loc, scale = 3.5, 1.3
    dist = stats.norm(loc=loc, scale=scale)
    rng = FastGeneratorInversion(dist, domain=(-1.5, 2))
    r = rng.rvs(size=100)
    lb, ub = loc - scale * 1.5, loc + scale * 2
    assert lb <= r.min() < r.max() <= ub

