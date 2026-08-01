
def test_from_quat_array_like():
    rng = np.random.default_rng(123)
    # Single rotation
    r_expected = Rotation.random(rng=rng)
    r = Rotation.from_quat(r_expected.as_quat().tolist())
    assert r_expected.approx_equal(r, atol=1e-12)

    # Multiple rotations
    r_expected = Rotation.random(3, rng=rng)
    r = Rotation.from_quat(r_expected.as_quat().tolist())
    assert np.all(r_expected.approx_equal(r, atol=1e-12))

    # Tensor of rotations
    q = rng.normal(size=(3, 4, 5, 4))
    q /= xp_vector_norm(q, axis=-1)[..., None]
    r_expected = Rotation.from_quat(q)
    r = Rotation.from_quat(q)
    assert np.all(r_expected.approx_equal(r, atol=1e-12))

