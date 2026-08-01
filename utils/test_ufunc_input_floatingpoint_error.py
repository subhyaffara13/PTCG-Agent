
def test_ufunc_input_floatingpoint_error(bad_offset):
    value = 123
    arr = np.array([value] * bad_offset +
                   [np.nan] +
                   [value] * int(1.5 * ncu.BUFSIZE))
    with np.errstate(invalid="raise"), pytest.raises(FloatingPointError):
        # Force cast inputs, but the buffered cast of `arr` to intp fails:
        np.add(arr, arr, dtype=np.intp, casting="unsafe")

