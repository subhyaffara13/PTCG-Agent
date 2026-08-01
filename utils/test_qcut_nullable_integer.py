
def test_qcut_nullable_integer(q, any_numeric_ea_dtype):
    arr = pd.array(np.arange(100), dtype=any_numeric_ea_dtype)
    arr[::2] = pd.NA

    result = qcut(arr, q)
    expected = qcut(arr.astype(float), q)

    tm.assert_categorical_equal(result, expected)

