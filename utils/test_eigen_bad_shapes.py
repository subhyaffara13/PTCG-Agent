
def test_eigen_bad_shapes():
    # A is not square.
    A = csc_array(np.zeros((2, 3)))
    assert_raises(ValueError, eigs, A)

