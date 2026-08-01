
def test_dropna_combinations(
    group_dropna, count_dropna, expected_rows, expected_values, request
):
    if not group_dropna:
        request.applymarker(
            pytest.mark.xfail(
                reason=(
                    "pandas default unstable sorting of duplicates"
                    "issue with numpy>=1.25 with AVX instructions"
                ),
                strict=False,
            )
        )
    nulls_df = DataFrame(
        {
            "A": [1, 1, np.nan, 4, np.nan, 6, 6, 6, 6],
            "B": [1, 1, 3, np.nan, np.nan, 6, 6, 6, 6],
            "C": [1, 2, 3, 4, 5, 6, np.nan, 8, np.nan],
            "D": [1, 2, 3, 4, 5, 6, 7, np.nan, np.nan],
        }
    )
    gp = nulls_df.groupby(["A", "B"], dropna=group_dropna)
    result = gp.value_counts(normalize=True, sort=True, dropna=count_dropna)
    columns = DataFrame()
    for column in nulls_df.columns:
        columns[column] = [nulls_df[column][row] for row in expected_rows]
    index = MultiIndex.from_frame(columns)
    expected = Series(data=expected_values, index=index, name="proportion")
    tm.assert_series_equal(result, expected)

