
def test_qspline2d(xp):
    rng = np.random.RandomState(181819143)
    image = rng.rand(71, 73)
    image = xp.asarray(image, dtype=xp_default_dtype(xp))
    result = signal.qspline2d(image)
    assert array_namespace(result) == xp

