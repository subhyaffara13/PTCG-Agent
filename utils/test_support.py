
def test_support(dist):
    """gh-6235"""
    dct = dict(distcont)
    args = dct[dist]

    dist = getattr(stats, dist)

    assert_almost_equal(dist.pdf(dist.a, *args), 0)
    assert_equal(dist.logpdf(dist.a, *args), -np.inf)
    assert_almost_equal(dist.pdf(dist.b, *args), 0)
    assert_equal(dist.logpdf(dist.b, *args), -np.inf)


def test_support(distname, args, expected):
    # test that the support is updated if truncation and loc/scale are applied
    # use beta distribution since it is a transformed betaprime distribution,
    # so it is important that the correct support is considered
    # (i.e., the support of beta is (0,1), while betaprime is (0, inf))
    dist = getattr(stats, distname)(*args)
    rng = FastGeneratorInversion(dist)
    assert_array_equal(rng.support(), expected)
    rng.loc = 1
    rng.scale = 2
    assert_array_equal(rng.support(), 1 + 2*np.array(expected))

