
def test_zero_rotation_get_set(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))

    r_get = r[xp.asarray([], dtype=xp.bool)]
    assert len(r_get) == 0

    r_slice = r[:0]
    assert len(r_slice) == 0

    with pytest.raises(IndexError):
        r[xp.asarray([0])]

    with pytest.raises(IndexError):
        r[xp.asarray([True])]

    with pytest.raises(IndexError):
        r[0] = Rotation.from_quat(xp.asarray([0, 0, 0, 1]))

