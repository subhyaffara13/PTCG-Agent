
def test_infer_dtype_pyarrow_dtype(data, request):
    res = lib.infer_dtype(data)
    assert res != "unknown-array"

    if data._hasna and res in ["datetime64", "timedelta64"]:
        mark = pytest.mark.xfail(
            reason="in infer_dtype pd.NA is not ignored in these cases "
            "even with skipna=True in the list(data) check below"
        )
        request.applymarker(mark)

    assert res == lib.infer_dtype(list(data), skipna=True)

