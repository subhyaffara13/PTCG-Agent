
def test_expand_dims():
    # Borrowed from Numpy tests.
    x = np.array([8.375, 7.545, 8.828, 8.5, 1.757, 5.928,
                  8.43, 7.78, 9.865, 5.878, 8.979, 4.732,
                  3.012, 6.022, 5.095, 3.116, 5.238, 3.957,
                  6.04, 9.63, 7.712, 3.382, 4.489, 6.479,
                  7.189, 9.645, 5.395, 4.961, 9.894, 2.893,
                  7.357, 9.828, 6.272, 3.758, 6.693, 0.993])
    npx = x.reshape(6, 6)
    sX = coo_array(npx)

    npx_expanded = np.expand_dims(npx, axis=1)
    sXexpanded = construct.expand_dims(sX, axis=1)
    assert_equal(sXexpanded[-1].toarray(), sX[-1, np.newaxis, :].toarray())
    assert_equal(sXexpanded.toarray(), npx_expanded)

    npxx = npx.reshape(3, 2, 2, 3)
    sXX = sX.reshape(3, 2, 2, 3)

    npxx_expanded = np.expand_dims(npxx, axis=2)
    sXXexpanded = construct.expand_dims(sXX, axis=2)
    assert_equal(sXXexpanded.shape, (3, 2, 1, 2, 3))
    assert_equal(sXXexpanded.toarray(), npxx_expanded)

    npxx_expanded = np.expand_dims(npxx, axis=-2)
    sXXexpanded = construct.expand_dims(sXX, axis=-2)
    assert_equal(sXXexpanded.shape, (3, 2, 2, 1, 3))
    assert_equal(sXXexpanded.toarray(), npxx_expanded)

