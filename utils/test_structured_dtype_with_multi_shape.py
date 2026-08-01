
def test_structured_dtype_with_multi_shape():
    dtype = np.dtype([("a", "u1", (2, 2))])
    data = StringIO("0 1 2 3\n")
    expected = np.array([(((0, 1), (2, 3)),)], dtype=dtype)
    assert_array_equal(np.loadtxt(data, dtype=dtype), expected)

