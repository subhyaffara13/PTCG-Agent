
def test_to_rgba_array_single_str():
    # single color name is valid
    assert_array_equal(mcolors.to_rgba_array("red"), [(1, 0, 0, 1)])

    # single char color sequence is invalid
    with pytest.raises(ValueError,
                       match="'rgb' is not a valid color value."):
        array = mcolors.to_rgba_array("rgb")

