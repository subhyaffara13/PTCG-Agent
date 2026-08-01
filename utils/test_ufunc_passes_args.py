
def test_ufunc_passes_args(func, arg, expected):
    # GH#40662
    arr = np.array([[1, 2], [3, 4]])
    df = pd.DataFrame(arr)
    result_inplace = np.zeros_like(arr)
    # 1-argument ufunc
    if arg is None:
        result = func(df, out=result_inplace)
    else:
        result = func(df, arg, out=result_inplace)

    expected = np.array(expected).reshape(2, 2)
    tm.assert_numpy_array_equal(result_inplace, expected)

    expected = pd.DataFrame(expected)
    tm.assert_frame_equal(result, expected)

