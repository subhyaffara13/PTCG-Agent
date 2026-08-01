
def test_bad_utf8():
    # Check that reader reads bad UTF with 'replace' option
    filename = pjoin(test_data_path,'broken_utf8.mat')
    res = loadmat(filename)
    assert_equal(res['bad_string'],
                 b'\x80 am broken'.decode('utf8', 'replace'))

