
def test_add_2d(any_string_dtype, request):
    dtype = any_string_dtype

    if dtype == object or dtype.storage == "pyarrow":
        reason = "Failed: DID NOT RAISE <class 'ValueError'>"
        mark = pytest.mark.xfail(raises=None, reason=reason)
        request.applymarker(mark)

    a = pd.array(["a", "b", "c"], dtype=dtype)
    b = np.array([["a", "b", "c"]], dtype=object)
    with pytest.raises(ValueError, match="3 != 1"):
        a + b

    s = Series(a)
    with pytest.raises(ValueError, match="3 != 1"):
        s + b

