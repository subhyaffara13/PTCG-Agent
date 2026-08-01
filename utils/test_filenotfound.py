
def test_filenotfound():
    # Check the correct error is thrown
    assert_raises(OSError, loadmat, "NotExistentFile00.mat")
    assert_raises(OSError, loadmat, "NotExistentFile00")

