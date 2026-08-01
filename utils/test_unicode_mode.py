
def test_unicode_mode():
    a = np.pad([1], 2, mode='constant')
    b = np.array([0, 0, 1, 0, 0])
    assert_array_equal(a, b)

