
def test_approx_equal_batched_input_validation(xp):
    p = Rotation.from_quat(xp.ones((2, 3, 4)))
    q = Rotation.from_quat(xp.ones((3, 2, 4)))
    with pytest.raises(ValueError, match="broadcastable shapes"):
        p.approx_equal(q)

    p = Rotation.from_quat(xp.ones((2, 4)))
    q = Rotation.from_quat(xp.ones((3, 4)))
    with pytest.raises(ValueError, match="broadcastable shapes"):
        p.approx_equal(q)

