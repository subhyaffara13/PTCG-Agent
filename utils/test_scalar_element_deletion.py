
def test_scalar_element_deletion():
    a = np.zeros(2, dtype=[('x', 'int'), ('y', 'int')])
    assert_raises(ValueError, a[0].__delitem__, 'x')

