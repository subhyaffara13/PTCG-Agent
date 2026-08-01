
def test_mat_dtype():
    double_eg = pjoin(test_data_path, 'testmatrix_6.1_SOL2.mat')
    fp = open(double_eg, 'rb')
    rdr = MatFile5Reader(fp, mat_dtype=False)
    d = rdr.get_variables()
    fp.close()
    assert_equal(d['testmatrix'].dtype.kind, 'u')

    fp = open(double_eg, 'rb')
    rdr = MatFile5Reader(fp, mat_dtype=True)
    d = rdr.get_variables()
    fp.close()
    assert_equal(d['testmatrix'].dtype.kind, 'f')

