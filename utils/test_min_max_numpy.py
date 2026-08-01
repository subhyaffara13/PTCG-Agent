
def test_min_max_numpy(method, box, dtype, request):
    if dtype.storage == "pyarrow" and box is pd.array:
        if box is pd.array:
            reason = "'<=' not supported between instances of 'str' and 'NoneType'"
        else:
            reason = "'ArrowStringArray' object has no attribute 'max'"
        mark = pytest.mark.xfail(raises=TypeError, reason=reason)
        request.applymarker(mark)

    arr = box(["a", "b", "c", None], dtype=dtype)
    result = getattr(np, method)(arr)
    expected = "a" if method == "min" else "c"
    assert result == expected

