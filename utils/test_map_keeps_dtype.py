
def test_map_keeps_dtype(na_action):
    # GH52219
    arr = Series(["a", np.nan, "b"])
    sparse_arr = arr.astype(pd.SparseDtype(object))
    df = DataFrame(data={"a": arr, "b": sparse_arr})

    def func(x):
        return str.upper(x) if not pd.isna(x) else x

    result = df.map(func, na_action=na_action)

    expected_sparse = pd.array(["A", np.nan, "B"], dtype=pd.SparseDtype(object))
    expected_arr = expected_sparse.astype(object)
    expected = DataFrame({"a": expected_arr, "b": expected_sparse})

    tm.assert_frame_equal(result, expected)

    result_empty = df.iloc[:0, :].map(func, na_action=na_action)
    expected_empty = expected.iloc[:0, :]
    tm.assert_frame_equal(result_empty, expected_empty)

