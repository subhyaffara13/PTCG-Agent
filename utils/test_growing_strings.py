
def test_growing_strings(dtype):
    # growing a string leads to a heap allocation, this tests to make sure
    # we do that bookkeeping correctly for all possible starting cases
    data = [
        "hello",  # a short string
        "abcdefghijklmnopqestuvwxyz",  # a medium heap-allocated string
        "hello" * 200,  # a long heap-allocated string
    ]

    arr = np.array(data, dtype=dtype)
    uarr = np.array(data, dtype=str)

    for _ in range(5):
        arr = arr + arr
        uarr = uarr + uarr

    assert_array_equal(arr, uarr)

