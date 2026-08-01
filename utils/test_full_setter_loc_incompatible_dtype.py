
def test_full_setter_loc_incompatible_dtype():
    # https://github.com/pandas-dev/pandas/issues/55791
    df = DataFrame({"a": [1, 2]})
    with pytest.raises(TypeError, match="Invalid value"):
        df.loc[:, "a"] = True

    with pytest.raises(TypeError, match="Invalid value"):
        df.loc[:, "a"] = {0: 3.5, 1: 4.5}

    df.loc[:, "a"] = {0: 3, 1: 4}
    expected = DataFrame({"a": [3, 4]})
    tm.assert_frame_equal(df, expected)

