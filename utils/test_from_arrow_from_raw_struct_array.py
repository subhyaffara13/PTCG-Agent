
def test_from_arrow_from_raw_struct_array():
    # in case pyarrow lost the Interval extension type (eg on parquet roundtrip
    # with datetime64[ns] subtype, see GH-45881), still allow conversion
    # from arrow to IntervalArray
    pa = pytest.importorskip("pyarrow")

    arr = pa.array([{"left": 0, "right": 1}, {"left": 1, "right": 2}])
    dtype = pd.IntervalDtype(np.dtype("int64"), closed="neither")

    result = dtype.__from_arrow__(arr)
    expected = IntervalArray.from_breaks(
        np.array([0, 1, 2], dtype="int64"), closed="neither"
    )
    tm.assert_extension_array_equal(result, expected)

    result = dtype.__from_arrow__(pa.chunked_array([arr]))
    tm.assert_extension_array_equal(result, expected)

