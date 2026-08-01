
def test_validate_sketch_error(value):
    with pytest.raises(ValueError, match="scale, length, randomness"):
        validate_sketch(value)
    with pytest.raises(ValueError, match="scale, length, randomness"):
        mpl.rcParams["path.sketch"] = value

