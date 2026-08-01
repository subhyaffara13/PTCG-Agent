
def test_swapaxes():
    # Borrowed from Numpy swapaxes tests
    x = np.array([8.375, 7.545, 8.828, 8.5, 1.757, 5.928,
                  8.43, 7.78, 9.865, 5.878, 8.979, 4.732,
                  3.012, 6.022, 5.095, 3.116, 5.238, 3.957,
                  6.04, 9.63, 7.712, 3.382, 4.489, 6.479,
                  7.189, 9.645, 5.395, 4.961, 9.894, 2.893,
                  7.357, 9.828, 6.272, 3.758, 6.693, 0.993])
    sX = coo_array(x).reshape(6, 6)
    sXswapped = construct.swapaxes(sX, 0, 1)
    assert_equal(sXswapped[-1].toarray(), sX[:, -1].toarray())

    sXX = sX.reshape(3, 2, 2, 3)
    sXXswapped = construct.swapaxes(sXX, 0, 2)
    assert_equal(sXXswapped.shape, (2, 2, 3, 3))

