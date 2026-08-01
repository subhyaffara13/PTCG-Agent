
def test_sort_uint():
    # Random data with NPY_MAX_UINT32 sprinkled
    rng = np.random.default_rng(42)
    N = 2047
    maxv = np.iinfo(np.uint32).max
    arr = rng.integers(low=0, high=maxv, size=N).astype('uint32')
    arr[np.random.choice(arr.shape[0], 10)] = maxv
    assert_equal(np.sort(arr, kind='quick'), np.sort(arr, kind='heap'))

