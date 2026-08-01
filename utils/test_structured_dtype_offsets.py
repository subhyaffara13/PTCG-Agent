
def test_structured_dtype_offsets():
    # An aligned structured dtype will have additional padding
    dt = np.dtype("i1, i4, i1, i4, i1, i4", align=True)
    data = StringIO("1,2,3,4,5,6\n7,8,9,10,11,12\n")
    expected = np.array([(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)], dtype=dt)
    assert_array_equal(np.loadtxt(data, delimiter=",", dtype=dt), expected)

