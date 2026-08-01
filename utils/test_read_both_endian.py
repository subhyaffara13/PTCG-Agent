
def test_read_both_endian():
    # make sure big- and little- endian data is read correctly
    for fname in ('big_endian.mat', 'little_endian.mat'):
        fp = open(pjoin(test_data_path, fname), 'rb')
        rdr = MatFile5Reader(fp)
        d = rdr.get_variables()
        fp.close()
        assert_array_equal(d['strings'],
                           np.array([['hello'],
                                     ['world']], dtype=object))
        assert_array_equal(d['floats'],
                           np.array([[2., 3.],
                                     [3., 4.]], dtype=np.float32))

