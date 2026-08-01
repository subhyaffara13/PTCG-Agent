
def test_from_euler_array_like():
    rng = np.random.default_rng(123)
    order = "xyz"
    # Single rotation
    r_expected = Rotation.random(rng=rng)
    r = Rotation.from_euler(order, r_expected.as_euler(order).tolist())
    assert r_expected.approx_equal(r, atol=1e-12)

    # Multiple rotations
    r_expected = Rotation.random(3, rng=rng)
    r = Rotation.from_euler(order, r_expected.as_euler(order).tolist())
    assert np.all(r_expected.approx_equal(r, atol=1e-12))

