
def test_mat73():
    # Check any hdf5 files raise an error
    filenames = glob(
        pjoin(test_data_path, 'testhdf5*.mat'))
    assert_(len(filenames) > 0)
    for filename in filenames:
        fp = open(filename, 'rb')
        assert_raises(NotImplementedError,
                      loadmat,
                      fp,
                      struct_as_record=True)
        fp.close()

