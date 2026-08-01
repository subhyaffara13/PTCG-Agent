
def test_nhypergeom_accuracy():
    # Check that nhypergeom.rvs post-gh-13431 gives the same values as
    # inverse transform sampling
    rng = np.random.RandomState(0)
    x = nhypergeom.rvs(22, 7, 11, size=100, random_state=rng)
    rng = np.random.RandomState(0)
    p = rng.uniform(size=100)
    y = nhypergeom.ppf(p, 22, 7, 11)
    assert_equal(x, y)

