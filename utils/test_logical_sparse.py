
def test_logical_sparse():
    # Test we can read logical sparse stored in mat file as bytes.
    # See https://github.com/scipy/scipy/issues/3539.
    # In some files saved by MATLAB, the sparse data elements (Real Part
    # Subelement in MATLAB speak) are stored with apparent type double
    # (miDOUBLE) but are in fact single bytes.
    filename = pjoin(test_data_path,'logical_sparse.mat')
    # Before fix, this would crash with:
    # ValueError: indices and data should have the same size
    d = loadmat(filename, struct_as_record=True, spmatrix=False)
    log_sp = d['sp_log_5_4']
    assert_(issparse(log_sp) and log_sp.format == "csc")
    assert_equal(log_sp.dtype.type, np.bool_)
    assert_array_equal(log_sp.toarray(),
                       [[True, True, True, False],
                        [False, False, True, False],
                        [False, False, True, False],
                        [False, False, False, False],
                        [False, False, False, False]])

