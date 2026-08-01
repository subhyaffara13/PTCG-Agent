
def test_where_none_nan_coerce():
    # GH 15613
    expected = DataFrame(
        {
            "A": [Timestamp("20130101"), pd.NaT, Timestamp("20130103")],
            "B": [1, 2, np.nan],
        }
    )
    result = expected.where(expected.notnull(), None)
    tm.assert_frame_equal(result, expected)

