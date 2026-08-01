
def test_invalid_rotation_values(rotation):
    with pytest.raises(
            ValueError,
            match=("rotation must be 'vertical', 'horizontal' or a number")):
        Text(0, 0, 'foo', rotation=rotation)

