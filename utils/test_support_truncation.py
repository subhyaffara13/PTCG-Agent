
def test_support_truncation(distname, args):
    # similar test for truncation
    dist = getattr(stats, distname)(*args)
    rng = FastGeneratorInversion(dist, domain=(0.5, 0.7))
    assert_array_equal(rng.support(), (0.5, 0.7))
    rng.loc = 1
    rng.scale = 2
    assert_array_equal(rng.support(), (1 + 2 * 0.5, 1 + 2 * 0.7))

