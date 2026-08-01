
def test_empty_sparse():
    # Can we read empty sparse matrices?
    sio = BytesIO()
    import scipy.sparse
    empty_sparse = scipy.sparse.csr_array([[0,0],[0,0]])
    savemat(sio, dict(x=empty_sparse))
    sio.seek(0)

    res = loadmat(sio, spmatrix=False)
    assert isinstance(res['x'], sparray)
    res = loadmat(sio, spmatrix=True)
    assert scipy.sparse.issparse(res['x']) and not isinstance(res['x'], sparray)
    with pytest.deprecated_call(match="The default value for `spmatrix"):
        res = loadmat(sio)  # chk default
        assert scipy.sparse.issparse(res['x']) and not isinstance(res['x'], sparray)

    assert_array_equal(res['x'].shape, empty_sparse.shape)
    assert_array_equal(res['x'].toarray(), 0)
    # Do empty sparse matrices get written with max nnz 1?
    # See https://github.com/scipy/scipy/issues/4208
    sio.seek(0)
    reader = MatFile5Reader(sio)
    reader.initialize_read()
    reader.read_file_header()
    hdr, _ = reader.read_var_header()
    assert_equal(hdr.nzmax, 1)

