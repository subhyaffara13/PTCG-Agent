
def test_is_level_reference_series_simple_axis0(df):
    # Make series with L1 as index
    s = df.set_index("L1").L2
    assert_level_reference(s, ["L1"], axis=0)
    assert not s._is_level_reference("L2")

    # Make series with L1 and L2 as index
    s = df.set_index(["L1", "L2"]).L3
    assert_level_reference(s, ["L1", "L2"], axis=0)
    assert not s._is_level_reference("L3")

