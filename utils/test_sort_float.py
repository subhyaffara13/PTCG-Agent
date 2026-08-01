
def test_sort_float(N, dtype):
    # Regular data with nan sprinkled
    np.random.seed(42)
    arr = -0.5 + np.random.sample(N).astype(dtype)
    arr[np.random.choice(arr.shape[0], 3)] = np.nan
    assert_equal(np.sort(arr, kind='quick'), np.sort(arr, kind='heap'))

    # (2) with +INF
    infarr = np.inf * np.ones(N, dtype=dtype)
    infarr[np.random.choice(infarr.shape[0], 5)] = -1.0
    assert_equal(np.sort(infarr, kind='quick'), np.sort(infarr, kind='heap'))

    # (3) with -INF
    neginfarr = -np.inf * np.ones(N, dtype=dtype)
    neginfarr[np.random.choice(neginfarr.shape[0], 5)] = 1.0
    assert_equal(np.sort(neginfarr, kind='quick'),
                 np.sort(neginfarr, kind='heap'))

    # (4) with +/-INF
    infarr = np.inf * np.ones(N, dtype=dtype)
    infarr[np.random.choice(infarr.shape[0], (int)(N / 2))] = -np.inf
    assert_equal(np.sort(infarr, kind='quick'), np.sort(infarr, kind='heap'))

