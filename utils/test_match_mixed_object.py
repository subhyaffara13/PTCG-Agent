
def test_match_mixed_object():
    mixed = Series(
        [
            "aBAD_BAD",
            np.nan,
            "BAD_b_BAD",
            True,
            datetime.today(),
            "foo",
            None,
            1,
            2.0,
        ]
    )
    result = Series(mixed).str.match(".*(BAD[_]+).*(BAD)")
    expected = Series([True, np.nan, True, np.nan, np.nan, False, None, np.nan, np.nan])
    assert isinstance(result, Series)
    tm.assert_series_equal(result, expected)

