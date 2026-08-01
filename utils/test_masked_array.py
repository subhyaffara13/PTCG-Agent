
def test_masked_array():
    a = np.ma.array([0, 1, 2, 3], mask=[0, 0, 1, 0])
    assert_equal(np.argwhere(a), [[1], [3]])

