
def test_miutf8_for_miint8_compromise():
    # Check reader accepts ascii as miUTF8 for array names
    filename = pjoin(test_data_path, 'miutf8_array_name.mat')
    res = loadmat(filename)
    assert_equal(res['array_name'], [[1]])
    # mat file with non-ascii utf8 name raises error
    filename = pjoin(test_data_path, 'bad_miutf8_array_name.mat')
    with assert_raises(ValueError):
        loadmat(filename)

