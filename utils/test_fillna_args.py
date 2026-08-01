
def test_fillna_args(dtype):
    # GH 37987

    arr = pd.array(["a", pd.NA], dtype=dtype)

    res = arr.fillna(value="b")
    expected = pd.array(["a", "b"], dtype=dtype)
    tm.assert_extension_array_equal(res, expected)

    res = arr.fillna(value=np.str_("b"))
    expected = pd.array(["a", "b"], dtype=dtype)
    tm.assert_extension_array_equal(res, expected)

    msg = "Invalid value '1' for dtype 'str"
    with pytest.raises(TypeError, match=msg):
        arr.fillna(value=1)

