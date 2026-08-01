
def test_permute_dims():
    # Borrowed from Numpy tests.
    x = np.array([8.375, 7.545, 8.828, 8.5, 1.757, 5.928,
                  8.43, 7.78, 9.865, 5.878, 8.979, 4.732,
                  3.012, 6.022, 5.095, 3.116, 5.238, 3.957,
                  6.04, 9.63, 7.712, 3.382, 4.489, 6.479,
                  7.189, 9.645, 5.395, 4.961, 9.894, 2.893,
                  7.357, 9.828, 6.272, 3.758, 6.693, 0.993])
    npx = x.reshape(6, 6)
    sX = coo_array(x).reshape(6, 6)

    sXpermuted = construct.permute_dims(sX, axes=(1, 0), copy=True)
    sXtransposed = sX.transpose(axes=(1, 0))
    assert_equal(sXpermuted.toarray(), sXtransposed.toarray())
    assert_equal(sXpermuted[-1].toarray(), sX[:, -1].toarray())

    npxx = npx.reshape(3, 2, 2, 3)
    sXX = sX.reshape(3, 2, 2, 3)
    sXXpermuted = construct.permute_dims(sXX, axes=(0, 2, 1, 3), copy=True)
    assert_equal(sXXpermuted.shape, (3, 2, 2, 3))
    sXXtransposed = sXX.transpose(axes=(0, 2, 1, 3))
    assert_equal(sXXtransposed.shape, (3, 2, 2, 3))
    assert_equal(sXXpermuted.toarray(), sXXtransposed.toarray())
    # TODO change np.transpose to np.permute_dims when numpy 2 is min supported version
    assert_equal(sXXpermuted.toarray(), np.transpose(npxx, axes=(0, 2, 1, 3)))

