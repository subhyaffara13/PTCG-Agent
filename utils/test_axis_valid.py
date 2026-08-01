
def test_axis_valid(axis):
    with pytest.raises(ValueError,
                       match="`axis` must be one of"):
        Rotation.create_group("C1", axis)

