
def test_argsort_largearrays(dtype):
    N = 1000000
    rnd = np.random.RandomState(1100710816)
    arr = -0.5 + rnd.random(N).astype(dtype)
    assert_arg_sorted(arr, np.argsort(arr, kind='quick'))

