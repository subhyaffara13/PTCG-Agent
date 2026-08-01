
def test_multiplication_errors(xp):
    rng = np.random.default_rng(0)
    r1 = Rotation.from_quat(xp.asarray(rng.normal(size=(2, 4))))
    r2 = Rotation.from_quat(xp.asarray(rng.normal(size=(1, 4, 4))))
    with pytest.raises(ValueError, match="Cannot broadcast"):
        r1 * r2

