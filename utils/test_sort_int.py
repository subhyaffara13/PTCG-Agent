
def test_sort_int(N, dtype):
    # Random data with MAX and MIN sprinkled
    minv = np.iinfo(dtype).min
    maxv = np.iinfo(dtype).max
    arr = np.random.randint(low=minv, high=maxv - 1, size=N, dtype=dtype)
    arr[np.random.choice(arr.shape[0], 10)] = minv
    arr[np.random.choice(arr.shape[0], 10)] = maxv
    assert_equal(np.sort(arr, kind='quick'), np.sort(arr, kind='heap'))

