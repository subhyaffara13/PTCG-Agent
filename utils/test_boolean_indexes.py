
def test_boolean_indexes(xp):
    r = rotation_to_xp(Rotation.random(3), xp)

    r0 = r[xp.asarray([False, False, False])]
    assert len(r0) == 0

    r1 = r[xp.asarray([False, True, False])]
    assert len(r1) == 1

    r3 = r[xp.asarray([True, True, True])]
    assert len(r3) == 3

    # Multiple dimensions
    r = Rotation.from_quat(xp.ones((3, 2, 4)))
    r4 = r[xp.asarray([True, False, False])]
    assert len(r4) == 1
    assert r4.as_quat().shape == (1, 2, 4)

    with pytest.raises(IndexError):
        r[xp.asarray([True, True])]

