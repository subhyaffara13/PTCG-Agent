
def test_ufunc_with_out_varied():
    """ Test that masked arrays are immune to gh-10459 """
    # the mask of the output should not affect the result, however it is passed
    a = array([ 1,  2,  3], mask=[1, 0, 0])
    b = array([10, 20, 30], mask=[1, 0, 0])
    out = array([ 0,  0,  0], mask=[0, 0, 1])
    expected = array([11, 22, 33], mask=[1, 0, 0])

    out_pos = out.copy()
    res_pos = np.add(a, b, out_pos)

    out_kw = out.copy()
    res_kw = np.add(a, b, out=out_kw)

    out_tup = out.copy()
    res_tup = np.add(a, b, out=(out_tup,))

    assert_equal(res_kw.mask,  expected.mask)
    assert_equal(res_kw.data,  expected.data)
    assert_equal(res_tup.mask, expected.mask)
    assert_equal(res_tup.data, expected.data)
    assert_equal(res_pos.mask, expected.mask)
    assert_equal(res_pos.data, expected.data)

