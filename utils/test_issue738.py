
def test_issue738():
    """Ignore strides on a length-1 dimension (even if they would be incompatible length > 1)"""
    assert np.all(m.iss738_f1(np.array([[1.0, 2, 3]])) == np.array([[1.0, 102, 203]]))
    assert np.all(
        m.iss738_f1(np.array([[1.0], [2], [3]])) == np.array([[1.0], [12], [23]])
    )

    assert np.all(m.iss738_f2(np.array([[1.0, 2, 3]])) == np.array([[1.0, 102, 203]]))
    assert np.all(
        m.iss738_f2(np.array([[1.0], [2], [3]])) == np.array([[1.0], [12], [23]])
    )

