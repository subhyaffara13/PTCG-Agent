
def test_partition_fp(N, dtype):
    rnd = np.random.RandomState(1100710816)
    arr = -0.5 + rnd.random(N).astype(dtype)
    k = rnd.choice(N, 1)[0]
    assert_arr_partitioned(np.sort(arr)[k], k,
            np.partition(arr, k, kind='introselect'))
    assert_arr_partitioned(np.sort(arr)[k], k,
            arr[np.argpartition(arr, k, kind='introselect')])

    # Check that `np.inf < np.nan`
    # This follows np.sort
    arr[0] = np.nan
    arr[1] = np.inf
    o1 = np.partition(arr, -2, kind='introselect')
    o2 = arr[np.argpartition(arr, -2, kind='introselect')]
    for out in [o1, o2]:
        assert_(np.isnan(out[-1]))
        assert_equal(out[-2], np.inf)

