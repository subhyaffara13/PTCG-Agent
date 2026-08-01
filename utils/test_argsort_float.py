
def test_argsort_float(N, dtype):
    rnd = np.random.RandomState(116112)
    # (1) Regular data with a few nan: doesn't use vectorized sort
    arr = -0.5 + rnd.random(N).astype(dtype)
    arr[rnd.choice(arr.shape[0], 3)] = np.nan
    assert_arg_sorted(arr, np.argsort(arr, kind='quick'))

    # (2) Random data with inf at the end of array
    # See: https://github.com/intel/x86-simd-sort/pull/39
    arr = -0.5 + rnd.rand(N).astype(dtype)
    arr[N - 1] = np.inf
    assert_arg_sorted(arr, np.argsort(arr, kind='quick'))

