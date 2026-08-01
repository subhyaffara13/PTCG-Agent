
def test_empty_transform_indexing(xp):
    tf_many = rigid_transform_to_xp(RigidTransform.identity(3), xp=xp)
    tf_zero = tf_many[xp.asarray([], dtype=xp.int32)]
    assert len(tf_zero) == 0

    # Array API does not specify out-of-bounds indexing. Only check for numpy.
    if is_numpy(xp):
        assert len(tf_zero[:5]) == 0  # Slices can go out of bounds.

    with pytest.raises(IndexError):
        tf_zero[0]

    with pytest.raises(IndexError):
        tf_zero[xp.asarray([0, 2])]

    with pytest.raises(IndexError):
        tf_zero[xp.asarray([False, True])]

