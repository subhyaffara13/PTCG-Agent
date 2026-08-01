
def test_group_type(name):
    with pytest.raises(ValueError,
                       match="must be a string"):
        Rotation.create_group(name)

