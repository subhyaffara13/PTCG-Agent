
def test_is_level_reference_series_axis1_error(df):
    # Make series with L1 as index
    s = df.set_index("L1").L2

    with pytest.raises(ValueError, match="No axis named 1"):
        s._is_level_reference("L1", axis=1)

