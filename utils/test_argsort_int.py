
def test_argsort_int(N, dtype):
    rnd = np.random.RandomState(1100710816)
    # (1) random data with min and max values
    minv = np.iinfo(dtype).min
    maxv = np.iinfo(dtype).max
    arr = rnd.randint(low=minv, high=maxv, size=N, dtype=dtype)
    i, j = rnd.choice(N, 2, replace=False)
    arr[i] = minv
    arr[j] = maxv
    assert_arg_sorted(arr, np.argsort(arr, kind='quick'))

    # (2) random data with max value at the end of array
    # See: https://github.com/intel/x86-simd-sort/pull/39
    arr = rnd.randint(low=minv, high=maxv, size=N, dtype=dtype)
    arr[N - 1] = maxv
    assert_arg_sorted(arr, np.argsort(arr, kind='quick'))

