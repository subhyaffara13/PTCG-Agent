
def test_one_by_zero():
    # Test 1x0 chars get read correctly
    func_eg = pjoin(test_data_path, 'one_by_zero_char.mat')
    fp = open(func_eg, 'rb')
    rdr = MatFile5Reader(fp)
    d = rdr.get_variables()
    fp.close()
    assert_equal(d['var'].shape, (0,))

