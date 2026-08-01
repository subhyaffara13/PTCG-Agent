
def test_zero_rotation_mean(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    with pytest.raises(ValueError, match="Mean of an empty rotation set is undefined."):
        r.mean()

