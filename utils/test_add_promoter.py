
def test_add_promoter(string_list):
    arr = np.array(string_list, dtype=StringDType())
    lresult = np.array(["hello" + s for s in string_list], dtype=StringDType())
    rresult = np.array([s + "hello" for s in string_list], dtype=StringDType())

    for op in ["hello", np.str_("hello"), np.array(["hello"])]:
        assert_array_equal(op + arr, lresult)
        assert_array_equal(arr + op, rresult)

    # The promoter should be able to handle things if users pass `dtype=`
    res = np.add("hello", string_list, dtype=StringDType)
    assert res.dtype == StringDType()

    # The promoter should not kick in if users override the input,
    # which means arr is cast, this fails because of the unknown length.
    with pytest.raises(TypeError, match="cannot cast dtype"):
        np.add(arr, "add", signature=("U", "U", None), casting="unsafe")

    # But it must simply reject the following:
    with pytest.raises(TypeError, match=".*did not contain a loop"):
        np.add(arr, "add", signature=(None, "U", None))

    with pytest.raises(TypeError, match=".*did not contain a loop"):
        np.add("a", "b", signature=("U", "U", StringDType))

