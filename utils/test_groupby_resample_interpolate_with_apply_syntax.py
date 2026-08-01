
def test_groupby_resample_interpolate_with_apply_syntax(groupy_test_df):
    # GH 35325

    # Make a copy of the test data frame that has index.name=None
    groupy_test_df_without_index_name = groupy_test_df.copy()
    groupy_test_df_without_index_name.index.name = None

    dfs = [groupy_test_df, groupy_test_df_without_index_name]

    for df in dfs:
        result = df.groupby("volume").apply(
            lambda x: x.resample("1D").interpolate(method="linear"),
        )

        volume = [50] * 15 + [60]
        week_starting = [
            *list(date_range("2018-01-07", "2018-01-21", unit="ns")),
            Timestamp("2018-01-14"),
        ]
        expected_ind = pd.MultiIndex.from_arrays(
            [volume, week_starting],
            names=["volume", df.index.name],
        )

        expected = DataFrame(
            data={
                "price": [
                    10.0,
                    9.928571428571429,
                    9.857142857142858,
                    9.785714285714286,
                    9.714285714285714,
                    9.642857142857142,
                    9.571428571428571,
                    9.5,
                    9.428571428571429,
                    9.357142857142858,
                    9.285714285714286,
                    9.214285714285714,
                    9.142857142857142,
                    9.071428571428571,
                    9.0,
                    11.0,
                ]
            },
            index=expected_ind,
        )
        tm.assert_frame_equal(result, expected)

