
def test_against_df_iloc(start, stop, step):
    # Test that a single group gives the same results as DataFrame.iloc
    n_rows = 30

    data = {
        "group": ["group 0"] * n_rows,
        "value": list(range(n_rows)),
    }
    df = pd.DataFrame(data)
    grouped = df.groupby("group", as_index=False)

    result = grouped._positional_selector[start:stop:step]
    expected = df.iloc[start:stop:step]

    tm.assert_frame_equal(result, expected)

