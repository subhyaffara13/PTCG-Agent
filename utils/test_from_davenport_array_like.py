
def test_from_davenport_array_like():
    rng = np.random.default_rng(123)
    # Single rotation
    e1 = np.array([1, 0, 0])
    e2 = np.array([0, 1, 0])
    e3 = np.array([0, 0, 1])
    r_expected = Rotation.random(rng=rng)
    angles = r_expected.as_davenport([e1, e2, e3], 'e')
    r = Rotation.from_davenport([e1, e2, e3], 'e', angles.tolist())
    assert r_expected.approx_equal(r, atol=1e-12)

    # Multiple rotations
    r_expected = Rotation.random(2, rng=rng)
    angles = r_expected.as_davenport([e1, e2, e3], 'e')
    r = Rotation.from_davenport([e1, e2, e3], 'e', angles.tolist())
    assert np.all(r_expected.approx_equal(r, atol=1e-12))

