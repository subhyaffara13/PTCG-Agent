
def test_drop_labels_or_levels_series(df):
    # Make series with L1 as index
    s = df.set_index("L1").L2
    assert_levels_dropped(s, ["L1"], axis=0)

    with pytest.raises(ValueError, match="not valid labels or levels"):
        s._drop_labels_or_levels("L4", axis=0)

    # Make series with L1 and L2 as index
    s = df.set_index(["L1", "L2"]).L3
    assert_levels_dropped(s, ["L1", "L2"], axis=0)

    with pytest.raises(ValueError, match="not valid labels or levels"):
        s._drop_labels_or_levels("L4", axis=0)

