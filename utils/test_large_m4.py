
def test_large_m4():
    # Test we can read a Matlab 4 file with array > 2GB.
    # (In fact, test we get the correct error from reading a truncated
    # version).
    # See https://github.com/scipy/scipy/issues/21256
    # Data file is first 1024 bytes of:
    # >>> a = np.zeros((134217728, 3))
    # >>> siom.savemat('big_m4.mat', {'a': a}, format='4')
    truncated_mat = pjoin(test_data_path, 'debigged_m4.mat')
    match = ("Not enough bytes to read matrix 'a';"
             if np.intp == np.int64 else
             "Variable 'a' has byte length longer than largest possible")
    with pytest.raises(ValueError, match=match):
        loadmat(truncated_mat)

