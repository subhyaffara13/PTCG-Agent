
def test_long_str():
    # check items larger than internal buffer size, gh-4027
    long_str_arr = np.ones(1, dtype=np.dtype((str, format.BUFFER_SIZE + 1)))
    long_str_arr2 = roundtrip(long_str_arr)
    assert_array_equal(long_str_arr, long_str_arr2)

