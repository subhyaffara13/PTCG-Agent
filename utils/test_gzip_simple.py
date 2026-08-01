
def test_gzip_simple():
    xdense = np.zeros((20,20))
    xdense[2,3] = 2.3
    xdense[4,5] = 4.5
    x = csc_array(xdense)

    name = 'gzip_test'
    expected = {'x':x}
    format = '4'

    tmpdir = mkdtemp()
    try:
        fname = pjoin(tmpdir,name)
        mat_stream = gzip.open(fname, mode='wb')
        savemat(mat_stream, expected, format=format)
        mat_stream.close()

        mat_stream = gzip.open(fname, mode='rb')
        actual = loadmat(mat_stream, struct_as_record=True, spmatrix=False)
        mat_stream.close()
    finally:
        shutil.rmtree(tmpdir)

    assert_array_almost_equal(actual['x'].toarray(),
                              expected['x'].toarray(),
                              err_msg=repr(actual))

