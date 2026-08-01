
def test_dropna(axis, val):
    df = DataFrame({"a": [1, 2, 3], "b": [4, val, 6], "c": "d"})
    df_orig = df.copy()
    df2 = df.dropna(axis=axis)

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_dropna():
    # GH 6194
    idx = MultiIndex.from_arrays(
        [
            [1, np.nan, 3, np.nan, 5],
            [1, 2, np.nan, np.nan, 5],
            ["a", "b", "c", np.nan, "e"],
        ]
    )

    exp = MultiIndex.from_arrays([[1, 5], [1, 5], ["a", "e"]])
    tm.assert_index_equal(idx.dropna(), exp)
    tm.assert_index_equal(idx.dropna(how="any"), exp)

    exp = MultiIndex.from_arrays(
        [[1, np.nan, 3, 5], [1, 2, np.nan, 5], ["a", "b", "c", "e"]]
    )
    tm.assert_index_equal(idx.dropna(how="all"), exp)

    msg = "invalid how option: xxx"
    with pytest.raises(ValueError, match=msg):
        idx.dropna(how="xxx")

    # GH26408
    # test if missing values are dropped for multiindex constructed
    # from codes and values
    idx = MultiIndex(
        levels=[[np.nan, None, pd.NaT, "128", 2], [np.nan, None, pd.NaT, "128", 2]],
        codes=[[0, -1, 1, 2, 3, 4], [0, -1, 3, 3, 3, 4]],
    )
    expected = MultiIndex.from_arrays([["128", 2], ["128", 2]])
    tm.assert_index_equal(idx.dropna(), expected)
    tm.assert_index_equal(idx.dropna(how="any"), expected)

    expected = MultiIndex.from_arrays(
        [[np.nan, np.nan, "128", 2], ["128", "128", "128", 2]]
    )
    tm.assert_index_equal(idx.dropna(how="all"), expected)


def test_dropna(fill_value):
    # GH-28287
    arr = SparseArray([np.nan, 1], fill_value=fill_value)
    exp = SparseArray([1.0], fill_value=fill_value)
    tm.assert_sp_array_equal(arr.dropna(), exp)

    df = pd.DataFrame({"a": [0, 1], "b": arr})
    expected_df = pd.DataFrame({"a": [1], "b": exp}, index=pd.Index([1]))
    tm.assert_equal(df.dropna(), expected_df)

