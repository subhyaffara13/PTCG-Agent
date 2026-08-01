
def test_group_order_positive(name):
    with pytest.raises(ValueError,
                       match="Group order must be positive"):
        Rotation.create_group(name)

