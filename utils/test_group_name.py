
def test_group_name(name):
    with pytest.raises(ValueError,
                       match="must be one of 'I', 'O', 'T', 'Dn', 'Cn'"):
        Rotation.create_group(name)

