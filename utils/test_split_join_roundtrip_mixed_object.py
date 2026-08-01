
def test_split_join_roundtrip_mixed_object():
    ser = Series(
        ["a_b", np.nan, "asdf_cas_asdf", True, datetime.today(), "foo", None, 1, 2.0]
    )
    result = ser.str.split("_").str.join("_")
    expected = Series(
        ["a_b", np.nan, "asdf_cas_asdf", np.nan, np.nan, "foo", None, np.nan, np.nan],
        dtype=object,
    )
    tm.assert_series_equal(result, expected)

