
def test_arrow_from_arrow_uint():
    # https://github.com/pandas-dev/pandas/issues/31896
    # possible mismatch in types

    dtype = pd.UInt32Dtype()
    result = dtype.__from_arrow__(pa.array([1, 2, 3, 4, None], type="int64"))
    expected = pd.array([1, 2, 3, 4, None], dtype="UInt32")

    tm.assert_extension_array_equal(result, expected)

