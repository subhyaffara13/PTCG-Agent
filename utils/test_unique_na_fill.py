
def test_unique_na_fill(arr, fill_value):
    a = SparseArray(arr, fill_value=fill_value).unique()
    b = pd.Series(arr).unique()
    assert isinstance(a, SparseArray)
    a = np.asarray(a)
    tm.assert_numpy_array_equal(a, b)

