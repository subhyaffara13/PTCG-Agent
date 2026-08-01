
def test_subclasses():
    # test that subclass is preserved only if subok=True
    a = VerySimpleSubClass([1, 2, 3, 4])
    assert_(type(a) is VerySimpleSubClass)
    a_view = as_strided(a, shape=(2,), strides=(2 * a.itemsize,))
    assert_(type(a_view) is np.ndarray)
    a_view = as_strided(a, shape=(2,), strides=(2 * a.itemsize,), subok=True)
    assert_(type(a_view) is VerySimpleSubClass)
    # test that if a subclass has __array_finalize__, it is used
    a = SimpleSubClass([1, 2, 3, 4])
    a_view = as_strided(a, shape=(2,), strides=(2 * a.itemsize,), subok=True)
    assert_(type(a_view) is SimpleSubClass)
    assert_(a_view.info == 'simple finalized')

    # similar tests for broadcast_arrays
    b = np.arange(len(a)).reshape(-1, 1)
    a_view, b_view = broadcast_arrays(a, b)
    assert_(type(a_view) is np.ndarray)
    assert_(type(b_view) is np.ndarray)
    assert_(a_view.shape == b_view.shape)
    a_view, b_view = broadcast_arrays(a, b, subok=True)
    assert_(type(a_view) is SimpleSubClass)
    assert_(a_view.info == 'simple finalized')
    assert_(type(b_view) is np.ndarray)
    assert_(a_view.shape == b_view.shape)

    # and for broadcast_to
    shape = (2, 4)
    a_view = broadcast_to(a, shape)
    assert_(type(a_view) is np.ndarray)
    assert_(a_view.shape == shape)
    a_view = broadcast_to(a, shape, subok=True)
    assert_(type(a_view) is SimpleSubClass)
    assert_(a_view.info == 'simple finalized')
    assert_(a_view.shape == shape)

