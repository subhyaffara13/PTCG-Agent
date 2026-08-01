
def test_rotation_shape(xp, ndim: int):
    shape = tuple(range(2, 2 + ndim)[:ndim - 1])
    quat = xp.ones(shape + (4,))
    r = Rotation.from_quat(quat)
    assert r.shape == shape, f"Got {r.shape}, expected {shape}"

