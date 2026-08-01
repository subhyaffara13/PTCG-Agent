
def test_multiindex_datetime_columns():
    # GH35015, using datetime as column indices raises exception

    mi = MultiIndex.from_tuples(
        [(to_datetime("02/29/2020"), to_datetime("03/01/2020"))], names=["a", "b"]
    )

    df = DataFrame([], columns=mi)

    expected_df = DataFrame(
        [],
        columns=MultiIndex.from_arrays(
            [[to_datetime("02/29/2020")], [to_datetime("03/01/2020")]], names=["a", "b"]
        ),
    )

    tm.assert_frame_equal(df, expected_df)

