
def test_partition_int(N, dtype):
    rnd = np.random.RandomState(1100710816)
    # (1) random data with min and max values
    minv = np.iinfo(dtype).min
    maxv = np.iinfo(dtype).max
    arr = rnd.randint(low=minv, high=maxv, size=N, dtype=dtype)
    i, j = rnd.choice(N, 2, replace=False)
    arr[i] = minv
    arr[j] = maxv
    k = rnd.choice(N, 1)[0]
    assert_arr_partitioned(np.sort(arr)[k], k,
            np.partition(arr, k, kind='introselect'))
    assert_arr_partitioned(np.sort(arr)[k], k,
            arr[np.argpartition(arr, k, kind='introselect')])

    # (2) random data with max value at the end of array
    arr = rnd.randint(low=minv, high=maxv, size=N, dtype=dtype)
    arr[N - 1] = maxv
    assert_arr_partitioned(np.sort(arr)[k], k,
            np.partition(arr, k, kind='introselect'))
    assert_arr_partitioned(np.sort(arr)[k], k,
            arr[np.argpartition(arr, k, kind='introselect')])

