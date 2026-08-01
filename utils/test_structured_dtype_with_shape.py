
def test_structured_dtype_with_shape():
    dtype = np.dtype([("a", "u1", 2), ("b", "u1", 2)])
    data = StringIO("0,1,2,3\n6,7,8,9\n")
    expected = np.array([((0, 1), (2, 3)), ((6, 7), (8, 9))], dtype=dtype)
    assert_array_equal(np.loadtxt(data, delimiter=",", dtype=dtype), expected)

