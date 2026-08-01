
def test_astype_from_non_pyarrow(data):
    # GH49795
    np_arr = data.to_numpy()
    pd_array = pd.array(np_arr, dtype=np_arr.dtype)
    result = pd_array.astype(data.dtype)
    assert not isinstance(pd_array.dtype, ArrowDtype)
    assert isinstance(result.dtype, ArrowDtype)
    tm.assert_extension_array_equal(result, data)

