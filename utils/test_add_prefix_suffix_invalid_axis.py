
def test_add_prefix_suffix_invalid_axis(string_series):
    with pytest.raises(ValueError, match="No axis named 1 for object type Series"):
        string_series.add_prefix("foo#", axis=1)

    with pytest.raises(ValueError, match="No axis named 1 for object type Series"):
        string_series.add_suffix("foo#", axis=1)


def test_add_prefix_suffix_invalid_axis(float_frame):
    with pytest.raises(ValueError, match="No axis named 2 for object type DataFrame"):
        float_frame.add_prefix("foo#", axis=2)

    with pytest.raises(ValueError, match="No axis named 2 for object type DataFrame"):
        float_frame.add_suffix("foo#", axis=2)

