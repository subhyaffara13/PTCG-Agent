
def test_len_and_bool(xp):
    rotation_multi_one = Rotation(xp.asarray([[0, 0, 0, 1]]))
    rotation_multi = Rotation(xp.asarray([[0, 0, 0, 1], [0, 0, 0, 1]]))
    rotation_single = Rotation(xp.asarray([0, 0, 0, 1]))

    assert len(rotation_multi_one) == 1
    assert len(rotation_multi) == 2
    with pytest.raises(TypeError, match="Single rotation has no len()."):
        len(rotation_single)

    rotation_batched = Rotation.from_quat(xp.ones((3, 2, 4)))
    assert len(rotation_batched) == 3

    # Rotation should always be truthy. See gh-16663
    assert rotation_multi_one
    assert rotation_multi
    assert rotation_single

