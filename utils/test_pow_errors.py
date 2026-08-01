
def test_pow_errors(xp):
    p = rotation_to_xp(Rotation.random(rng=0), xp)
    with pytest.raises(NotImplementedError, match='modulus not supported'):
        pow(p, 1, 1)
    with pytest.raises(ValueError, match="Array exponent must be a scalar"):
        p ** xp.asarray([1, 2])
    with pytest.raises(ValueError, match="Array exponent must be a scalar"):
        p ** xp.asarray([[1], [2]])

