
def test_ufunc_input_casterrors(bad_offset):
    value = 123
    arr = np.array([value] * bad_offset +
                   ["string"] +
                   [value] * int(1.5 * ncu.BUFSIZE), dtype=object)
    with pytest.raises(ValueError):
        # Force cast inputs, but the buffered cast of `arr` to intp fails:
        np.add(arr, arr, dtype=np.intp, casting="unsafe")

