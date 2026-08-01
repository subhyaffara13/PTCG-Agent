
def test_from_quat_wrong_shape(xp, ndim: int):
    quat = xp.zeros((*((1,) * ndim), 5))
    with pytest.raises(ValueError, match="Expected `quat` to have shape"):
        Rotation.from_quat(quat)

