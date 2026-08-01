
def test_construct_from_string_fill_value_raises(string):
    with pytest.raises(TypeError, match="fill_value in the string is not"):
        SparseDtype.construct_from_string(string)

