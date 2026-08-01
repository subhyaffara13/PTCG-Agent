
def test_rsh():
    rng = np.random.default_rng(806795795)
    x = rng.standard_normal(100)
    res = ms.rsh(x)
    # Just a sanity check that the code runs and output shape is correct.
    # TODO: check that implementation is correct.
    assert_(res.shape == x.shape)

    # Check points keyword
    res = ms.rsh(x, points=[0, 1.])
    assert_(res.size == 2)

