
def test_aesara_function_numpy():
    """ Test aesara_function() vs Numpy implementation. """
    f = aesara_function_([x, y], [x+y], dim=1,
                         dtypes={x: 'float64', y: 'float64'})
    assert np.linalg.norm(f([1, 2], [3, 4]) - np.asarray([4, 6])) < 1e-9

    f = aesara_function_([x, y], [x+y], dtypes={x: 'float64', y: 'float64'},
                         dim=1)
    xx = np.arange(3).astype('float64')
    yy = 2*np.arange(3).astype('float64')
    assert np.linalg.norm(f(xx, yy) - 3*np.arange(3)) < 1e-9

