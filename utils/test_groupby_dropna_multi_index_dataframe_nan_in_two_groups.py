
def test_groupby_dropna_multi_index_dataframe_nan_in_two_groups(
    dropna, tuples, outputs, nulls_fixture, nulls_fixture2
):
    # GH 3729 this is to test that NA in different groups with different representations
    df_list = [
        ["A", "B", 12, 12, 12],
        ["A", nulls_fixture, 12.3, 233.0, 12],
        ["B", "A", 123.23, 123, 1],
        [nulls_fixture2, "B", 1, 1, 1.0],
        ["A", nulls_fixture2, 1, 1, 1.0],
    ]
    df = pd.DataFrame(df_list, columns=["a", "b", "c", "d", "e"])
    grouped = df.groupby(["a", "b"], dropna=dropna).sum()

    mi = pd.MultiIndex.from_tuples(tuples, names=list("ab"))

    # Since right now, by default MI will drop NA from levels when we create MI
    # via `from_*`, so we need to add NA for level manually afterwards.
    if not dropna:
        mi = mi.set_levels([["A", "B", np.nan], ["A", "B", np.nan]])
    expected = pd.DataFrame(outputs, index=mi)

    tm.assert_frame_equal(grouped, expected)

