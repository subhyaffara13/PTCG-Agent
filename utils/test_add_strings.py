
def test_add_strings(any_string_dtype, request):
    dtype = any_string_dtype
    if dtype != np.dtype(object):
        mark = pytest.mark.xfail(reason="GH-28527")
        request.applymarker(mark)
    arr = pd.array(["a", "b", "c", "d"], dtype=dtype)
    df = pd.DataFrame([["t", "y", "v", "w"]], dtype=object)
    assert arr.__add__(df) is NotImplemented

    result = arr + df
    expected = pd.DataFrame([["at", "by", "cv", "dw"]]).astype(dtype)
    tm.assert_frame_equal(result, expected)

    result = df + arr
    expected = pd.DataFrame([["ta", "yb", "vc", "wd"]]).astype(dtype)
    tm.assert_frame_equal(result, expected)

