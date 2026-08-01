
def test_masked_mixed_types(dtype1, dtype2, exp_col1, exp_col2):
    # GH#37506
    data1 = [1.0, np.nan] if dtype1.startswith("f") else [1.0, pd.NA]
    data2 = [1.0, np.nan] if dtype2.startswith("f") else [1.0, pd.NA]
    df = DataFrame(
        {"col1": pd.array(data1, dtype=dtype1), "col2": pd.array(data2, dtype=dtype2)}
    )
    result = df.groupby([1, 1]).agg("all", skipna=False)

    expected = DataFrame({"col1": exp_col1, "col2": exp_col2}, index=np.array([1]))
    tm.assert_frame_equal(result, expected)

