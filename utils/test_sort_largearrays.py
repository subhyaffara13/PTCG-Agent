
def test_sort_largearrays(dtype):
    N = 1000000
    rnd = np.random.RandomState(1100710816)
    arr = -0.5 + rnd.random(N).astype(dtype)
    assert_equal(np.sort(arr, kind='quick'), np.sort(arr, kind='heap'))

