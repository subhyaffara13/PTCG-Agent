
def test_func_read():
    func_eg = pjoin(test_data_path, 'testfunc_7.4_GLNX86.mat')
    fp = open(func_eg, 'rb')
    rdr = MatFile5Reader(fp)
    d = rdr.get_variables()
    fp.close()
    assert isinstance(d['testfunc'], MatlabFunction)
    stream = BytesIO()
    wtr = MatFile5Writer(stream)
    # This test mat file has `__header__` field.
    with pytest.warns(MatWriteWarning, match='Starting field name with'):
        assert_raises(MatWriteError, wtr.put_variables, d)

