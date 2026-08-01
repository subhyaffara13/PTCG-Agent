
def test_check_label_or_level_ambiguity_series_axis1_error(df):
    # Make series with L1 as index
    s = df.set_index("L1").L2

    with pytest.raises(ValueError, match="No axis named 1"):
        s._check_label_or_level_ambiguity("L1", axis=1)

