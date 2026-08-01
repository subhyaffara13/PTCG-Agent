
def test_memory_usage_empty_no_warning(using_infer_string):
    # GH#50066
    df = DataFrame(index=["a", "b"])
    with tm.assert_produces_warning(None):
        result = df.memory_usage()
    if using_infer_string and HAS_PYARROW:
        value = 18
    else:
        value = 16 if IS64 else 8
    expected = Series(value, index=["Index"])
    tm.assert_series_equal(result, expected)

