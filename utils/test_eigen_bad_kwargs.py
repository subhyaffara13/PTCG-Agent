
def test_eigen_bad_kwargs():
    # Test eigen on wrong keyword argument
    A = csc_array(np.zeros((8, 8)))
    assert_raises(ValueError, eigs, A, which='XX')

