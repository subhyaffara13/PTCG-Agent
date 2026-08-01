
def test_1d_shape():
    # New 5 behavior is 1D -> row vector
    arr = np.arange(5)
    for format in ('4', '5'):
        # Column is the default
        stream = BytesIO()
        savemat(stream, {'oned': arr}, format=format)
        vals = loadmat(stream)
        assert_equal(vals['oned'].shape, (1, 5))
        # can be explicitly 'column' for oned_as
        stream = BytesIO()
        savemat(stream, {'oned':arr},
                format=format,
                oned_as='column')
        vals = loadmat(stream)
        assert_equal(vals['oned'].shape, (5,1))
        # but different from 'row'
        stream = BytesIO()
        savemat(stream, {'oned':arr},
                format=format,
                oned_as='row')
        vals = loadmat(stream)
        assert_equal(vals['oned'].shape, (1,5))

