
def test_concat_dense_sparse():
    # GH 30668
    dtype = pd.SparseDtype(np.float64, None)
    a = Series(pd.arrays.SparseArray([1, None]), dtype=dtype)
    b = Series([1], dtype=float)
    expected = Series(data=[1, None, 1], index=[0, 1, 0]).astype(dtype)
    result = concat([a, b], axis=0)
    tm.assert_series_equal(result, expected)

