
def test_flatiter_indexing():
    # see gh-29659
    arr = np.array(['hello', 'world'], dtype='T')
    arr.flat[:] = 9223372036854775
    assert_array_equal(arr, np.array([9223372036854775] * 2, dtype='T'))

