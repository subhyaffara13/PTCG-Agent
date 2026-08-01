
def test_cspline2d(xp):
    rng = np.random.RandomState(181819142)
    image = rng.rand(71, 73)
    image = xp.asarray(image, dtype=xp_default_dtype(xp))
    result = signal.cspline2d(image, 8.0)
    assert array_namespace(result) == xp

