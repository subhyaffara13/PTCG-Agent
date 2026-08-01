
def test_wide_to_long_string_columns(string_storage):
    # GH 57066
    string_dtype = pd.StringDtype(string_storage, na_value=np.nan)
    df = DataFrame(
        {
            "ID": {0: 1},
            "R_test1": {0: 1},
            "R_test2": {0: 1},
            "R_test3": {0: 2},
            "D": {0: 1},
        }
    )
    df.columns = df.columns.astype(string_dtype)
    result = wide_to_long(
        df, stubnames="R", i="ID", j="UNPIVOTED", sep="_", suffix=".*"
    )
    expected = DataFrame(
        [[1, 1], [1, 1], [1, 2]],
        columns=Index(["D", "R"]),
        index=pd.MultiIndex.from_arrays(
            [
                [1, 1, 1],
                Index(["test1", "test2", "test3"], dtype=string_dtype),
            ],
            names=["ID", "UNPIVOTED"],
        ),
    )
    tm.assert_frame_equal(result, expected)

