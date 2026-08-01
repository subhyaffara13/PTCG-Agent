
def test_array_constructors():
    data = np.arange(1, 7, dtype="int32")
    for i in range(8):
        np.testing.assert_array_equal(m.test_array_ctors(10 + i), data.reshape((3, 2)))
        np.testing.assert_array_equal(m.test_array_ctors(20 + i), data.reshape((3, 2)))
    for i in range(5):
        np.testing.assert_array_equal(m.test_array_ctors(30 + i), data)
        np.testing.assert_array_equal(m.test_array_ctors(40 + i), data)

