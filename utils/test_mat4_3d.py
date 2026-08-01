
def test_mat4_3d():
    # test behavior when writing 3-D arrays to matlab 4 files
    stream = BytesIO()
    arr = np.arange(24).reshape((2,3,4))
    assert_raises(ValueError, savemat, stream, {'a': arr}, True, '4')

