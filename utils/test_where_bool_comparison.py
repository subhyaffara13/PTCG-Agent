
def test_where_bool_comparison():
    # GH 10336
    df_mask = DataFrame(
        {"AAA": [True] * 4, "BBB": [False] * 4, "CCC": [True, False, True, False]}
    )
    result = df_mask.where(df_mask == False)  # noqa: E712
    expected = DataFrame(
        {
            "AAA": np.array([np.nan] * 4, dtype=object),
            "BBB": [False] * 4,
            "CCC": [np.nan, False, np.nan, False],
        }
    )
    tm.assert_frame_equal(result, expected)

