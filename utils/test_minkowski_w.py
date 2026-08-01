
def test_minkowski_w():
    # Regression test for gh-8142.
    arr_in = np.array([[83.33333333, 100., 83.33333333, 100., 36.,
                        60., 90., 150., 24., 48.],
                       [83.33333333, 100., 83.33333333, 100., 36.,
                        60., 90., 150., 24., 48.]])
    p0 = pdist(arr_in, metric='minkowski', p=1, w=None)
    c0 = cdist(arr_in, arr_in, metric='minkowski', p=1, w=None)
    p1 = pdist(arr_in, metric='minkowski', p=1)
    c1 = cdist(arr_in, arr_in, metric='minkowski', p=1)

    assert_allclose(p0, p1, rtol=1e-15)
    assert_allclose(c0, c1, rtol=1e-15)

