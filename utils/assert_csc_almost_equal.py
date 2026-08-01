
def assert_csc_almost_equal(r, l):
    r = csc_array(r)
    l = csc_array(l)
    assert_equal(r.indptr, l.indptr)
    assert_equal(r.indices, l.indices)
    assert_array_almost_equal_nulp(r.data, l.data, 10000)

