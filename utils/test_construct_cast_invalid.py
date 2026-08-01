
def test_construct_cast_invalid(dtype):
    msg = "cannot safely"
    arr = [1.2, 2.3, 3.7]
    with pytest.raises(TypeError, match=msg):
        pd.array(arr, dtype=dtype)

    with pytest.raises(TypeError, match=msg):
        pd.Series(arr).astype(dtype)

    arr = [1.2, 2.3, 3.7, pd.NA]
    with pytest.raises(TypeError, match=msg):
        pd.array(arr, dtype=dtype)

    with pytest.raises(TypeError, match=msg):
        pd.Series(arr).astype(dtype)

