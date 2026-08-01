
def test_ufunc_binary_output(using_nan_is_na):
    a = pd.array([1, 2, pd.NA], dtype="Int64")
    result = np.modf(a)
    np_res = np.modf(a.to_numpy(na_value=np.nan, dtype="float"))

    np_res = list(np_res)
    np_res[0] = np_res[0].astype(object)
    np_res[1] = np_res[1].astype(object)
    np_res[0][-1] = pd.NA
    np_res[1][-1] = pd.NA

    expected = (pd.array(np_res[0]), pd.array(np_res[1]))

    assert isinstance(result, tuple)
    assert len(result) == 2

    for x, y in zip(result, expected, strict=True):
        tm.assert_extension_array_equal(x, y)

