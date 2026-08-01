
def test_from_euler_scalar():
    rng = np.random.default_rng(123)
    deg = rng.uniform(low=-180, high=180)
    r_expected = Rotation.from_euler("x", deg, degrees=True)
    r = Rotation.from_euler("x", float(deg), degrees=True)
    assert r_expected.approx_equal(r, atol=1e-12)

