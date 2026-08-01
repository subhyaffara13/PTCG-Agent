
def test_nd_todense(shape):
    np.random.seed(12)
    arr = np.random.randint(low=0, high=5, size=shape)
    assert_equal(coo_array(arr).todense(), arr)

