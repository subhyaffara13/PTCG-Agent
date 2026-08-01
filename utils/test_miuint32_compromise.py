
def test_miuint32_compromise():
    # Reader should accept miUINT32 for miINT32, but check signs
    # mat file with miUINT32 for miINT32, but OK values
    filename = pjoin(test_data_path, 'miuint32_for_miint32.mat')
    res = loadmat(filename)
    assert_equal(res['an_array'], np.arange(10)[None, :])
    # mat file with miUINT32 for miINT32, with negative value
    filename = pjoin(test_data_path, 'bad_miuint32.mat')
    with assert_raises(ValueError):
        loadmat(filename)

