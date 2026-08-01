
def test_mixed_string_comparison_ufuncs_fail(op, ufunc, sym):
    arr_string = np.array(["a", "b"], dtype="S")
    arr_unicode = np.array(["a", "c"], dtype="U")

    with pytest.raises(TypeError, match="did not contain a loop"):
        ufunc(arr_string, arr_unicode)

    with pytest.raises(TypeError, match="did not contain a loop"):
        ufunc(arr_unicode, arr_string)

